__author__ = 'luiz'

from flask_restful import abort as rest_abort, wraps
from flask import request


class ApiAuth(object):

    def __init__(self, *args, **kwargs):
        self.role = kwargs.get("role")

    def login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if LoginManager.validate_token(
                    request.environ.get('HTTP_API_TOKEN'), self.role):
                return func(*args, **kwargs)
            rest_abort(401)
        return wrapper


class LoginManager(object):

    @staticmethod
    def do_login(user, password):
        pass

    @staticmethod
    def do_logout(api_token):
        pass

    @staticmethod
    def validate_token(api_token, role=None):
        return True
