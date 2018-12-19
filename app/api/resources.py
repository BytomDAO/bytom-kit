from flask_restful import Resource
from flask_restful import reqparse
from app.model.hello import get_hello_result
from app.model.signature import sign
from app.model.signature import verify
from app.model.key import create_entropy
from app.model.key import entropy_to_mnemonic

parser = reqparse.RequestParser()
parser.add_argument('private_key', type=str)
parser.add_argument('message', type=str)
parser.add_argument('public_key', type=str)
parser.add_argument('signature', type=str)
parser.add_argument('entropy_str', type=str)

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

class Verify(Resource):
    
    def post(self):
        args = parser.parse_args()
        public_key = args.get('public_key')
        signature = args.get('signature')
        message = args.get('message')
        result = verify(public_key, signature, message)
        return result

class Create_Entropy(Resource):

    def post(self):
        entropy = create_entropy()
        return entropy

class Entropy_To_Mnemonic(Resource):

    def post(self):
        args = parser.parse_args()
        entropy_str = args.get('entropy_str')
        mnemonic_str = entropy_to_mnemonic(entropy_str)
        return mnemonic_str