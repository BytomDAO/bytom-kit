from flask_restful import Resource
from app.model.hello import get_hello_result


class Hello(Resource):

    def get(self, content):
        return get_hello_result(content)
