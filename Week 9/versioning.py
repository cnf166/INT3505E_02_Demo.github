from flask import Flask, jsonify

app = Flask(__name__)

# ===== API v1 =====

@app.route('/api/v1/users', methods=['GET'])
def get_users_v1():
    """v1: Returns simple user data"""
    return jsonify({
        'users': [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'}
        ]
    })


@app.route('/api/v1/users/<int:user_id>', methods=['GET'])
def get_user_v1(user_id):
    """v1: Get single user"""
    return jsonify({
        'id': user_id,
        'name': f'User {user_id}'
    })


# ===== API v2 - Enhanced Version =====

@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    """v2: Returns enhanced user data with metadata"""
    return jsonify({
        'status': 'success',
        'data': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ],
        'count': 2
    })


@app.route('/api/v2/users/<int:user_id>', methods=['GET'])
def get_user_v2(user_id):
    """v2: Get single user with email"""
    return jsonify({
        'status': 'success',
        'data': {
            'id': user_id,
            'name': f'User {user_id}',
            'email': f'user{user_id}@example.com'
        }
    })


# ===== APPROACH 2: QUERY PARAMETER VERSIONING =====

@app.route('/api/users', methods=['GET'])
def get_users_query_param():
    """Query parameter versioning - version passed as ?version=1 or ?version=2"""
    from flask import request
    version = request.args.get('version', '1')
    
    if version == '2':
        # v2 response
        return jsonify({
            'status': 'success',
            'data': [
                {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
            ],
            'count': 2
        })
    else:
        # v1 response (default)
        return jsonify({
            'users': [
                {'id': 1, 'name': 'Alice'},
                {'id': 2, 'name': 'Bob'}
            ]
        })


# ===== APPROACH 3: HEADER-BASED VERSIONING =====

@app.route('/api/users/header', methods=['GET'])
def get_users_header_based():
    """Header-based versioning - version in Accept header"""
    from flask import request
    
    # Check Accept header for version
    accept_header = request.headers.get('Accept', 'application/vnd.api.v1+json')
    
    if 'v2' in accept_header:
        # v2 response
        return jsonify({
            'status': 'success',
            'data': [
                {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
                {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
            ],
            'count': 2
        })
    else:
        # v1 response (default)
        return jsonify({
            'users': [
                {'id': 1, 'name': 'Alice'},
                {'id': 2, 'name': 'Bob'}
            ]
        })


if __name__ == '__main__':
    print("""
    
    APPROACH 1 - URL PATH VERSIONING:
    ✓ http://localhost:5000/api/v1/users
    ✓ http://localhost:5000/api/v2/users
    
    APPROACH 2 - QUERY PARAMETER VERSIONING:
    ✓ http://localhost:5000/api/users?version=1
    ✓ http://localhost:5000/api/users?version=2
    
    APPROACH 3 - HEADER-BASED VERSIONING:
    ✓ curl -H "Accept: application/vnd.api.v1+json" http://localhost:5000/api/users/header
    ✓ curl -H "Accept: application/vnd.api.v2+json" http://localhost:5000/api/users/header
    """)
    app.run(debug=True)
