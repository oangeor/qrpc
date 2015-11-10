# coding=utf-8
import json


class RpcResponseBase(object):
    """
    An RpcResponse baseclass

    This class doesn't handle content. It should not be used directly.
    Use the it's subclasses instead.
    """
    rpc_code = 0
    result = None
    message = None

    def __init__(self, result=None, error_code=None, message=None):
        self.result = result
        if error_code:
            self.rpc_code = int(error_code)
        self.message = message

    @property
    def to_dict(self):
        return {
            'rpc_code': self.rpc_code,
            'message': self.message or '',
            'data': self.result
        }


class RpcResponse(RpcResponseBase):
    rpc_code = 0


class RpcResponseMethodNotFound(RpcResponseBase):
    rpc_code = -2

    def __init__(self, method):
        message = 'method {} not found'.format(json.dumps(method)),

        super(RpcResponseMethodNotFound, self).__init__(message=message)


class RpcResponseError(RpcResponseBase):
    def __init__(self, error_code, error_message):
        super(RpcResponseError, self).__init__(error_code=error_code, message=error_message)


class RpcResponseUnexpected(RpcResponseBase):
    rpc_code = -1

    def __init__(self, message):
        # TODO: debug message
        super(RpcResponseUnexpected, self).__init__(message=message)


class RpcResponseList(object):
    def __init__(self):
        self._response_list = []

    def append(self, response):
        assert isinstance(response, RpcResponseBase)
        self._response_list.append(response)

    def to_json(self):
        """
        Convert reponse list to json.
        """
        json_list = []
        for response in self._response_list:
            json_list.append(response.to_dict)

        return json.dumps(json_list)
