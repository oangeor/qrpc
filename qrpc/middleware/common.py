# coding=utf-8
import traceback

from qrpc.exceptions import RPCFaultException
from qrpc.response import RpcResponse
from qrpc.response import RpcResponseError
from qrpc.response import RpcResponseMethodNotFound
from qrpc.response import RpcResponseUnexpected


class CommonMiddleware(object):
    """
    "Common" middleware for taking care of some basic operations:
    """

    @staticmethod
    def process_request(rpc_method):
        if not rpc_method:
            return RpcResponseMethodNotFound(rpc_method.endpoint)

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

    @staticmethod
    def process_response(response):
        """
        Do nothing for now.
        """
        return response
