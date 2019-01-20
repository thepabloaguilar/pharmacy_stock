from flask import Flask

from api import backend

def create_app():
    app = Flask(__name__)

    app.register_blueprint(backend.api_bp, url_prefix=f'/api')

    return app
