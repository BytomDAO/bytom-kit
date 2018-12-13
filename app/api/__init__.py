from flask import Blueprint
from flask_restful import Api

from app.api.resources import Hello
from app.api.resources import Sign
from app.api.resources import Verify

blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
api = Api(blueprint)

api.add_resource(Hello, '/hello/<string:content>')
api.add_resource(Sign, '/sign')
api.add_resource(Verify, '/verify')