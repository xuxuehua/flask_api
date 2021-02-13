from flask import Flask, request, Blueprint
from flask_restful import reqparse, Api, Resource
import json

from api_response import http201
from operators import firewalld_configuration

app = Flask(__name__)
api = Api(app)


class ApiRequestArgs(Resource):

    def post_request(self, **all_args):
        if isinstance(all_args, None):
            raise RuntimeError('invalid post')

    def _post_request(self, all_args, **url_kwargs):
        if request.method == 'POST':
            request_args = json.loads(request.get_data())
        else:
            request_args = {}
            for key, values in dict(request.args).items():
                if isinstance(values, (list, tuple)):
                    request_args[key] = values[0]
                else:
                    request_args[key] = values

        request_args.update(url_kwargs)
        return all_args(**request_args)

    def post(self, **url_kwargs):
        return self._post_request(self.post_request, **url_kwargs)


class ADD(ApiRequestArgs):
    def post_request(self, **all_args):
        firewalld_configuration(ip=all_args['ip'],
                                src_port=all_args['src_port'],
                                dest_port=all_args['dest_port'])
        return http201(message="OK", data=all_args)


api.add_resource(ADD, '/add/<string:ip>')


if __name__ == '__main__':
    app.run(debug=True, port=5000)
