# Features
* Easy registration of methods
* Custom Exception and Options
* Includes plenty testing helpers

# Installation
On most systems, its a matter of
```bash
pip setup.py install
```

# Quickstart
## A Simple Example
This is a realy simple example of how to create your own API using QRpc

### Server

```python
from qrpc.server import Server

server = Server()


@server.registe("service1/hello")
def hello(name=None):
    if name:
        return "hello " + name
    return "hello anonymous"


@server.registe("service1/add")
def add(x, y):
    return x + y


server.run('127.0.0.1', 8080)
```


### Client

```python
from qrpc.client import RpcClient
from qrpc.client import ServerProxy

server = ServerProxy('http://localhost:8080/v1/batch')
rpc = RpcClient(server=server)
result = rpc.service1.hello.call(name='ycc')
print(result.data)

```
# Core content
## Request


## Response(Result)
The response of an rpc request has three attributes that user should concern, rpc_code, data, message.

The rpc_code indicates if the rpc request has been successfully received, understood, and accepted. 0 and all the positive numbers are **reserved code**, and can't be used by user.

The data is the result of an rpc method.

The message provides some helpful information.


## Exceptions
You can define an RPCException and raise it when you want to tell the caller there is something wrong in some rpc method. For example a division rpc method and the second argument of a division is zero.

```python
# server
from qrpc.exceptions import RPCFaultException
@server.registe("service/div")
def test_div(x, y):
    if y == 0:
        raise RPCFaultException(
        code=99, # Use any code in your as you like except reserved code.
        message="ZeroDivisionError: integer division or modulo by zero"
    )
    return x / y

# client
div_result = rpc.service.div.call(x=1, y=0)
```

The QRpc will catch the exception and wrap it in reponse.




# Lazy Call and Evaluation

RPC call are lazy--the act of creating an rpc call doesn't send the network request to server. You can stack call together all day long, and the framework won't actually send the network request until one of the calls is evaluated. You can get detail from the following example:

```python
    add_result = rpc.service.add.call(x=1, y=2)
    dict_result = rpc.service.dictionary.call(dictionary={"test_key": "test_value"})
    hello_result = rpc.service.hello.call(name='world')
    print (add_result.data) # only one network request
    print (dict_result.data)
    print (hello_result.data)
```

Though this looks like sending three rpc call request, in fact it only send one network request, at the "add_result.data" line. An rpc call is just added into a job list when it is constructed. The real network request will be executed when any of the 'rcp call' in the job list is evaluated. The framework evaluates all the rpc call in the job list at one time. So only send one network request.You can evaluate an rpc call by get any attribute of the rcp result.

In the last example, there are three rpc calls in the job list. The three rpc calls are evaluated at one network request when you get the data of add_result.
So dict_result.data or hello_result.data won't cause any network request.

In general, the result of an rpc call isn't fetched from the server until you ask them.

# Adcanced Usage
# TODO