from flask import Flask

def create_app():
    app = Flask(__name__)

    from .fda import fda
    from .teoria import teoria

    app.register_blueprint(teoria, url_prefix='/')
    app.register_blueprint(fda, url_prefix='/')
    
    return app

