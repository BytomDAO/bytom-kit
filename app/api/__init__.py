from flask import Blueprint
from flask_restful import Api

from app.api.resources import Hello

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(Hello, '/hello/<string:content>')
