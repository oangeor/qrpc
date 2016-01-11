# coding=utf-8
import functools
import json
import traceback

import requests

from qrpc.exceptions import RPCCommunicationException
from qrpc.request import RpcRequest
from qrpc.result import Lazy
from qrpc.result import RpcResult
from qrpc.scheduler import SchedulerBatch

HTTP_SUCCESS = 200


class ServerProxy(object):
    def __init__(self, uri, version='v1'):
        self._uri = uri

    def _request(self, params):
        return requests.post(
            url=self._uri,
            data=params,
        )

    def run_request(self, params):
        try:
            response = self._request(params)
        except requests.ConnectionError as e:
            raise RPCCommunicationException(message=traceback.format_exc())

        if HTTP_SUCCESS != response.status_code:
            raise RPCCommunicationException(message="invalid http status code: {}".format(response.status_code))

        result_list = []
        response_list = json.loads(response.text)
        for resp in response_list:
            rpc_result = RpcResult(
                rpc_code=resp['rpc_code'],
                message=resp['message'],
                data=resp['data'],
            )
            result_list.append(rpc_result)
        return result_list


class RpcClient(object):
    def __init__(self, host, port=80):
        uri = " http://{}:{}/v1/batch".format(host, port)
        server = ServerProxy(uri=uri)
        self._scheduler = SchedulerBatch(
            server
        )
        self._server = server

    def __getattr__(self, attr):
        return _Callable(self, attr)

    def invoke(self, method, params):
        req = RpcRequest(
            method=method,
            params=params
        )
        scheduler = self._scheduler
        job = self._scheduler.add_request(req)
        result = Lazy(functools.partial(scheduler.get_result, job))

        return result


class _Executable(object):
    def __init__(self, client, method):
        self._client = client
        self._method = method

    def __call__(self, **kwargs):
        return self._client.invoke(method=self._method, params=kwargs)

    def __str__(self):
        return '_Executable (%s)' % (self._method)

    __repr__ = __str__


class _Callable(object):
    def __init__(self, client, name):
        self._client = client
        self._name = name

    def __getattr__(self, attr):
        if attr == 'call':
            return _Executable(self._client, self._name)
        name = '%s/%s' % (self._name, attr)
        return _Callable(self._client, name)

    def __str__(self):
        return '_Callable (%s)' % self._name

    __repr__ = __str__
