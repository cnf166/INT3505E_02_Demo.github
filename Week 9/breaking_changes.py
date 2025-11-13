from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)

# ===== v2 (DEPRECATED) =====

@app.route('/api/v2/users', methods=['GET'])
def get_users_v2():
    """v2: Old format (DEPRECATED)"""
    response = jsonify({
        'users': [
            {'id': 1, 'name': 'Alice'},
            {'id': 2, 'name': 'Bob'}
        ]
    })
    # Add deprecation headers
    response.headers['Deprecation'] = 'true'
    response.headers['Sunset'] = '2025-06-01'
    response.headers['Link'] = '</api/v3/users>; rel="successor-version"'
    return response


# ===== v3 (CURRENT - BREAKING CHANGES) =====

@app.route('/api/v3/users', methods=['GET'])
def get_users_v3():
    """v3: New format (BREAKING CHANGES from v2)"""
    return jsonify({
        'version': '3.0',
        'timestamp': datetime.utcnow().isoformat(),
        'data': [
            {'id': 1, 'name': 'Alice', 'email': 'alice@example.com'},
            {'id': 2, 'name': 'Bob', 'email': 'bob@example.com'}
        ]
    })


# ===== INFO =====

@app.route('/api', methods=['GET'])
def api_info():
    """API versions"""
    return jsonify({
        'versions': {
            'v2': {
                'status': 'deprecated',
                'sunset': '2025-06-01',
                'breaking_changes': [
                    'Response structure changed',
                    'Fields moved inside data wrapper'
                ]
            },
            'v3': {
                'status': 'current',
                'endpoint': '/api/v3/users',
                'new_fields': ['version', 'timestamp']
            }
        }
    })


if __name__ == '__main__':
    app.run(debug=True)
