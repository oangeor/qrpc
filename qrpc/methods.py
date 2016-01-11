# coding=utf-8
import re

import six

from qrpc.exceptions import RPCSystemException


class MethodBindError(RPCSystemException):
    pass


class RpcMethod(object):
    __valid_endpoint_re = re.compile(r'^(_|[a-z][a-z0-9_]*)(/[a-z][a-z0-9_]*)+$')

    def __init__(self, fn, endpoint, options):
        assert callable(fn)
        assert isinstance(endpoint, six.string_types)
        if not self.__valid_endpoint_re.match(endpoint):
            raise MethodBindError('invalid endpoint name: {}'.format(endpoint))

        self.fn = fn
        self.endpoint = endpoint
        self.service = self.endpoint.split('/', 1)[0]
        self.options = options

    def __call__(self, *args, **kwargs):
        return self.fn(*args, **kwargs)


class RpcMethodMap(object):
    def __init__(self):
        self.__method_map = {}

    def add(self, method):
        """
        Add the registed rpc function.
        """
        assert isinstance(method, RpcMethod)
        if method.endpoint in self.__method_map:
            raise MethodBindError(
                'different function bound to same endpoint: endpoint={endpoint}, {method_1}, {method_2}'.format(
                    endpoint=method.endpoint,
                    method_1=self.__method_map[method.endpoint],
                    method_2=method,
                )
            )
        self.__method_map[method.endpoint] = method

    def get_method_function(self, endpoint):
        method = self.__method_map.get(endpoint)
        return method

    def __iter__(self):
        return six.iteritems(self.__method_map)
