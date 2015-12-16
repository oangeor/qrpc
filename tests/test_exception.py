# coding=utf-8
import threading

from qrpc.client import RpcClient
from qrpc.server import Server


def test_fault_exception():
    from qrpc.exceptions import RPCFaultException
    HOST_PORT = ('127.0.0.1', 8080)
    zero_division_error = RPCFaultException(
        code=99,
        message="ZeroDivisionError: integer division or modulo by zero"
    )

    server = Server()

    @server.registe("service/div")
    def test_div(x, y):
        if y == 0:
            raise zero_division_error
        return x / y

    t = threading.Thread(target=server.run, args=HOST_PORT)
    t.setDaemon(True)
    t.start()

    rpc = RpcClient(*HOST_PORT)
    div_result = rpc.service.div.call(x=1, y=0)
    try:
        div_result.data
    except RPCFaultException as e:
        assert e.code == zero_division_error.code
        assert e.message == zero_division_error.message


def test_communication_exception():
    from qrpc.exceptions import RPCCommunicationException

    SERVER_HOST_PORT = ('127.0.0.1', 8080)
    CLIENT_HOST_PORT = ('127.0.0.1', 9090)
    server = Server()

    @server.registe("service/hello")
    def test_hello(name=None):
        if name:
            return "hello " + name
        return "hello anonymous"

    t = threading.Thread(target=server.run, args=SERVER_HOST_PORT)
    t.setDaemon(True)
    t.start()

    rpc = RpcClient(*CLIENT_HOST_PORT)
    hello_result = rpc.service.hello.call(name="world")
    try:
        hello_result.data
    except RPCCommunicationException as e:
        pass
    else:
        # Make sure that rpc call must throw RPCCommunicationException
        raise
