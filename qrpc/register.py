# coding=utf-8
from __future__ import unicode_literals, absolute_import
def registe(endpoint, **options):
    def decorator(fn):
        method = RpcMethod(fn, endpoint, options)
        method_map.add(method=method)
        return fn
    return decorator