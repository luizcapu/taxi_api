__author__ = 'luiz'

from flask_restful import abort as rest_abort, wraps
from base import BaseResource


def authenticate(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        from flask import request
        r = request.environ.get('HTTP_API_TOKEN')
        if not getattr(func, 'authenticated', True):
            return func(*args, **kwargs)

        acct = r is not None  # custom account lookup function
        if acct:
            return func(*args, **kwargs)

        rest_abort(401)
    return wrapper


class LoggedAsDriverResource(BaseResource):
    method_decorators = [authenticate]
