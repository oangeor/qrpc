# coding=utf-8
# from qrpc.middleware.base import BaseMiddleware


class DeprecatedMiddleware(object):
    """
    Deprecated middleware that show deprecated method warning
    """
    option_name = 'deprecated'

    @staticmethod
    def process_response(response):
        response.message = "DeprecatedWarning: This rpc method will no longer be supported"
        return response