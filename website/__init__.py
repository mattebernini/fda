from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


def create_app():
    app = Flask(__name__)

    from .fda import fda
    app.register_blueprint(fda, url_prefix='/fda')
    
    return app

