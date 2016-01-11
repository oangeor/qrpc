# coding=utf-8


class RpcRequest(object):
    def __init__(self, method, params):
        self._method = method
        self._params = params

    @property
    def method(self):
        return self._method

    @property
    def params(self):
        return self._params

    @property
    def to_json(self):
        return {
            'method': self._method,
            'params': self._params
        }
