from flask import Flask 

from .extensions import api, db
from .resources import ns

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-in-production'

    api = Api(app, version='3.0', title='Library Management API',
            description='Version 3: Stateless Architecture Demo',
            authorizations={
                'Bearer': {
                    'type': 'apiKey',
                    'in': 'header',
                    'name': 'Authorization',
                    'description': 'JWT token format: Bearer <token>'
                }
            })

    ns = api.namespace('api/v3', description='Stateless operations')

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)

    return app