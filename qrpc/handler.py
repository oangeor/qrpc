# coding=utf-8
import functools

import six

from qrpc.methods import RpcMethodMap
from qrpc.middleware import OPTIONS_MIDDLEWARE
from qrpc.middleware.common import CommonMiddleware
from qrpc.request import RpcRequest


class RpcHandler(object):
    """
    Handle the rpc request.
    It takes the rpc request data, dispatches the method, and send it back to client.
    """

    def __init__(self, method_map):
        assert isinstance(method_map, RpcMethodMap)
        self._method_map = method_map
        self._request_middleware_list = [CommonMiddleware().process_request]
        self._response_middleware_list = [CommonMiddleware().process_response]

    support_options = OPTIONS_MIDDLEWARE

    def _load_middleware(self, options):
        """
        Populate middleware lists from options
        """

        for option_name, option_value in six.iteritems(options):
            middleware_instance = self.support_options[option_name]
            if hasattr(middleware_instance, 'process_request'):
                mw_process = functools.partial(middleware_instance.process, option_value=option_value)
                self._request_middleware_list.append(mw_process)
            if hasattr(middleware_instance, 'process_response'):
                self._response_middleware_list.insert(0, middleware_instance.process_response)

    def get_response(self, rpc_request):
        assert isinstance(rpc_request, RpcRequest)
        rpc_method = self._method_map.get_method_function(rpc_request.method)
        self._load_middleware(rpc_method.options)
        response = None
        rpc_method = functools.partial(rpc_method, **rpc_request.params)
        for middleware_method in self._request_middleware_list:
            response = middleware_method(rpc_method)

        for middleware_method in self._response_middleware_list:
            response = middleware_method(response)
        return response
