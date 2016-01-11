# coding=utf-8
from __future__ import unicode_literals, absolute_import

from qrpc.exceptions import RPCFaultException
from qrpc.exceptions import RPCSystemException


class Lazy(object):
    def __init__(self, evaluator):
        assert callable(evaluator)
        self._evaluator = evaluator
        self._evaluated = False
        self._result_cache = None

    def __getattr__(self, name):
        if self._result_cache is not None:
            return self._result_cache[name]
        self._result_cache = self._evaluator()
        return self._result_cache[name]


class RpcResult(object):
    def __init__(self, rpc_code, data, message):
        self._data = data
        self._rpc_code = rpc_code
        self._message = message

    def raise_for_code(self):
        if self._rpc_code == -1:
            raise RPCSystemException(message=self._message)
        if self._rpc_code > 0:
            raise RPCFaultException(code=self._rpc_code, message=self._message)

    def __getitem__(self, item):
        self.raise_for_code()
        if item == 'data':
            return self._data
        if item == 'rpc_code':
            return self._rpc_code
        if item == 'message':
            return self._message

        raise KeyError
