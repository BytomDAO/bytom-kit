from flask_restful import Resource
from flask_restful import reqparse
from app.model.hello import get_hello_result
from app.model.signature import sign
from app.model.signature import verify

parser = reqparse.RequestParser()
parser.add_argument('private_key', type=str)
parser.add_argument('message', type=str)

class Hello(Resource):

    def get(self, content):
        return get_hello_result(content)

class Sign(Resource):

    def post(self):
        args = parser.parse_args()
        private_key = args.get('private_key')
        message = args.get('message')
        sig = sign(private_key, message)
        return sig
