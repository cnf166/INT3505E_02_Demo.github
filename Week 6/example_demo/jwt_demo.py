import jwt
import datetime

# Secret key (production)
SECRET_KEY = 'your-secret-key'
# Payload
payload = {
    'user': 'testuser',
    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
}
# Encode JWT
token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
print("Generated Token:", token)

# Decode JWT
try:
    decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    print("Decoded Payload:", decoded)
except jwt.ExpiredSignatureError:
    print("Token has expired")
except jwt.InvalidTokenError:
    print("Invalid token")