from flask import Flask, request, jsonify, make_response
from flask_cors import CORS
import jwt
import datetime

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SECRET_KEY'] = 'cookie-secret-key'

def create_token(user_id):
    return jwt.encode({
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    }, app.config['SECRET_KEY'], algorithm='HS256')

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if data.get('username') == 'user' and data.get('password') == 'pass':
        token = create_token(1)
        resp = make_response(jsonify({'message': 'Logged in with HttpOnly cookie'}))
        resp.set_cookie(
            'access_token',
            token,
            httponly=True,
            secure=False,  # Đổi thành True nếu dùng HTTPS
            samesite='Lax',
            max_age=15*60
        )
        return resp
    return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
def protected():
    token = request.cookies.get('access_token')
    if not token:
        return jsonify({'message': 'Token missing'}), 401
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return jsonify({'message': f'Hello user {payload["user_id"]}! (HttpOnly Cookie)'})
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401

@app.route('/logout', methods=['POST'])
def logout():
    resp = make_response(jsonify({'message': 'Logged out'}))
    resp.set_cookie('access_token', '', expires=0)
    return resp

if __name__ == '__main__':
    app.run(port=5003, debug=True)