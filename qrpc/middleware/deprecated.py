# coding=utf-8
# from qrpc.middleware.base import BaseMiddleware


class DeprecatedMiddleware(object):
    """
    Deprecated middleware that show deprecated method warning
    """
    option_name = 'deprecated'

    # def process_request(self, fn, option_value):
    #     result = fn()
    #     if option_value is True:
    #         raise

    def process_response(self, response):
        response.message = "DeprecatedWarning: This rpc method will no longer be supported"
        return response