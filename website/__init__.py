from flask import Flask


def create_app():
    app = Flask(__name__)

    from .fda import fda
    app.register_blueprint(fda, url_prefix='/')
    
    return app

