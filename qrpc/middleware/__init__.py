# coding=utf-8

from .deprecated import DeprecatedMiddleware

OPTIONS_MIDDLEWARE = {
    DeprecatedMiddleware.option_name: DeprecatedMiddleware
}
