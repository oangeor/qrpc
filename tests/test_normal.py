# coding=utf-8
import threading

from qrpc.client import RpcClient
from qrpc.server import Server


def test_normal():
    HOST_PORT = ('127.0.0.1', 8080)
    server = Server()

    @server.registe("service/hello")
    def test_hello(name=None):
        if name:
            return "hello " + name
        return "hello anonymous"

    @server.registe("service/add")
    def test_add(x, y):
        return x + y

    @server.registe("service/dictionary")
    def test_dictionary(dictionary):
        return dictionary

    t = threading.Thread(target=server.run, args=HOST_PORT)
    t.setDaemon(True)
    t.start()

    rpc = RpcClient(*HOST_PORT)
    add_result = rpc.service.add.call(x=1, y=2)
    dict_result = rpc.service.dictionary.call(dictionary={"test_key": "test_value"})
    hello_result = rpc.service.hello.call(name='world')

    assert add_result.data == 3
    assert dict_result.data["test_key"] == "test_value"
    assert hello_result.data == "hello world"
