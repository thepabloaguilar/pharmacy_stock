from flask import Flask
from flasgger import Swagger

from api import backend

def create_app():
    app = Flask(__name__)

    app.register_blueprint(backend.api_bp, url_prefix=f'/api')

    app.config['SWAGGER'] = {
        'uiversion': 3,
        'swagger_version': '3.0',
        'title': 'Pharmacy Stock API',
        'specs_route': '/docs',
        'description': 'Routes to administrate API'
    }

    Swagger(app=app)

    return app
