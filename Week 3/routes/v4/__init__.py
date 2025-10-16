from flask import Flask 

from .extensions import api, db
from .resources import ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='4.0', title='Library Management API',
            description='Version 4: Cacheable Architecture Demo')

    ns = api.namespace('api/v4', description='Cacheable operations')

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    api.init_app(app)
    db.init_app(app)

    api.add_namespace(ns)

    return app