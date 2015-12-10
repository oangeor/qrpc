# coding=utf-8

import six


# class RPCException(Exception):
#     pass


class RPCFaultException(Exception):
    def __init__(self, code, message):
        assert isinstance(code, six.integer_types)
        assert isinstance(message, six.string_types)
        self.code = code
        self.message = six.text_type(message)

        super(RPCFaultException, self).__init__('[{}]{}'.format(
            self.code,
            self.message,
        ))

    @property
    def error(self):
        return {
            'rpc_code': self.code,
            'message': self.message
        }


class RPCSystemException(Exception):
    def __init__(self, message=None, debug_message=None):
        super(RPCSystemException, self).__init__(message)


class RPCCommunicationException(RPCSystemException):
    """
    Could not connect to server or invalid http status_code
    """
    pass
