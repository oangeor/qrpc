# coding=utf-8
from qrpc.request import RpcRequest


class Job(object):
    def __init__(self, req):
        assert isinstance(req, RpcRequest)
        self.req = req
        self.result = None
