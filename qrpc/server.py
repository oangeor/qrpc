# coding=utf-8
import json
from wsgiref.simple_server import make_server

import falcon

from qrpc.handler import RpcHandler
from qrpc.methods import RpcMethod
from qrpc.methods import RpcMethodMap
from qrpc.request import RpcRequest
from qrpc.response import RpcResponseList


class BatchHandler(object):
    def __init__(self, rpc_handler):
        self._rpc_handler = rpc_handler

    def on_post(self, req, resp):
        """Handles the HTTP POST request.

        Attempts to interpret all HTTP POST requests as RPC calls,
        which are forwarded to the  rpc_handler for handling.
        """
        assert isinstance(req, falcon.Request)
        assert isinstance(resp, falcon.Response)
        requests_json = ','.join(req.get_param_as_list('requests', required=True))
        request_value = json.loads(requests_json)
        response_list = RpcResponseList()
        for one_request in request_value:
            request = RpcRequest(
                method=one_request['method'],
                params=one_request['params'],
            )
            response = self._rpc_handler.get_response(request)
            response_list.append(response)
        response_body = response_list.to_json()
        print(response_body)
        resp.content_type = 'application/json'
        resp.body = response_body


class Server(object):
    def __init__(self):
        self._wsgi_app = falcon.API()
        self.method_map = RpcMethodMap()
        self.rpc_handler = RpcHandler(self.method_map)
        self._wsgi_set_up()

    def _wsgi_set_up(self):
        self._wsgi_app.req_options.auto_parse_form_urlencoded = True
        self._wsgi_app.add_route('/v1/batch', BatchHandler(self.rpc_handler))

    def __call__(self, env, start_response):
        return self._wsgi_app(env, start_response)

    def run(self, host, port):
        """Create a new  server listening on `host` and `port` for `app`"""

        wsgi_server = make_server(host=host, port=port, app=self._wsgi_app)
        try:
            wsgi_server.serve_forever()
        finally:
            wsgi_server.server_close()

    def registe(self, endpoint, **options):
        """
        Register a function to response to RPC requests.

        """

        def decorator(fn):
            method = RpcMethod(fn, endpoint, options)
            self.method_map.add(method=method)
            return fn

        return decorator

    def server_list_method(self):
        pass
