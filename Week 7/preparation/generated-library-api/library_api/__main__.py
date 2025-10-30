# library_api/__main__.py
import connexion
from flask_cors import CORS
from library_api import encoder
from library_api.database import init_db

def main():
    app = connexion.App(__name__, specification_dir='./swagger/')
    app.app.json_encoder = encoder.JSONEncoder
    app.add_api('swagger.yaml', arguments={'title': 'Library Management API'}, pythonic_params=True)
    
    # Enable CORS
    CORS(app.app)
    
    # Initialize database
    init_db(app.app)
    
    app.run(port=5000, debug=True)

if __name__ == '__main__':
    main()