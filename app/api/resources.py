from flask_restful import Resource
from flask_restful import reqparse
from app.model.hello import get_hello_result
from app.model.signature import sign
from app.model.signature import verify
from app.model.key import create_entropy
from app.model.key import entropy_to_mnemonic
from app.model.key import mnemonic_to_seed
from app.model.key import seed_to_root_xprv
from app.model.key import xprv_to_expanded_private_key
from app.model.key import xpub_to_public_key
from app.model.key import xpub_verify

parser = reqparse.RequestParser()
parser.add_argument('private_key_str', type=str)
parser.add_argument('message_str', type=str)
parser.add_argument('public_key_str', type=str)
parser.add_argument('signature_str', type=str)
parser.add_argument('entropy_str', type=str)
parser.add_argument('mnemonic_str', type=str)
parser.add_argument('seed_str', type=str)
parser.add_argument('xprv_str', type=str)
parser.add_argument('xpub_str', type=str)

class Hello(Resource):

    def get(self, content):
        return get_hello_result(content)

class Sign(Resource):

    def post(self):
        args = parser.parse_args()
        private_key = args.get('private_key_str')
        message = args.get('message_str')
        sig = sign(private_key, message)
        return sig

class Verify(Resource):
    
    def post(self):
        args = parser.parse_args()
        public_key = args.get('public_key_str')
        signature = args.get('signature_str')
        message = args.get('message_str')
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

class Mnemonic_To_Seed(Resource):

    def post(self):
        args = parser.parse_args()
        mnemonic_str = args.get('mnemonic_str')
        seed_str = mnemonic_to_seed(mnemonic_str)
        return seed_str

class Seed_To_Root_Xprv(Resource):

    def post(self):
        args = parser.parse_args()
        seed_str = args.get('seed_str')
        root_xprv_str = seed_to_root_xprv(seed_str)
        return root_xprv_str

class Xprv_To_Expanded_Private_Key(Resource):

    def post(self):
        args = parser.parse_args()
        xprv_str = args.get('xprv_str')
        expanded_private_key_str = xprv_to_expanded_private_key(xprv_str)
        return expanded_private_key_str

class Xpub_To_Public_Key(Resource):

    def post(self):
        args = parser.parse_args()
        xpub_str = args.get('xpub_str')
        public_key_str = xpub_to_public_key(xpub_str)
        return public_key_str

class Xpub_Verify(Resource):

    def post(self):
        args = parser.parse_args()
        xpub = args.get('xpub_str')
        message = args.get('message_str')
        signature = args.get('signature_str')
        result = xpub_verify(xpub, message, signature)
        return result