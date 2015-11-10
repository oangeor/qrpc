# coding=utf-8
import functools
import traceback

from qrpc.exceptions import RPCFaultException
from qrpc.methods import RpcMethodMap
from qrpc.request import RpcRequest
from qrpc.response import RpcResponse
from qrpc.response import RpcResponseError
from qrpc.response import RpcResponseUnexpected


class Dispatcher(object):

    def __init__(self, method_map):
        assert isinstance(method_map, RpcMethodMap)
        self._method_map = method_map

    def get_response(self, rpc_request):
        assert isinstance(rpc_request, RpcRequest)
        rpc_method = self._method_map.get_method_function(rpc_request.method)
        response = None
        rpc_method = functools.partial(rpc_method, **rpc_request.params)
        try:
            result = rpc_method()
            response = RpcResponse(
                result=result
            )
        except RPCFaultException as e:
            response = RpcResponseError(
                error_code=e.code,
                error_message=e.message
            )
        except Exception as e:
            format_exc = traceback.format_exc()

            response = RpcResponseUnexpected(
                message=format_exc
            )
        return response
