# coding=utf-8
import threading

from qrpc.client import RpcClient
from qrpc.server import Server


def test_middleware():
    HOST_POST = ('127.0.0.1', 8080)
    server = Server()

    @server.registe("service/hello", deprecated=True)
    def test_hello(name=None):
        if name:
            return "hello " + name
        return "hello anonymous"

    t = threading.Thread(target=server.run, args=HOST_POST)
    t.setDaemon(True)
    t.start()

    rpc = RpcClient(*HOST_POST)
    hello_result = rpc.service.hello.call(name='world')

    assert hello_result.data == "hello world"
    assert hello_result.message.startswith("DeprecatedWarning") is True
