__author__ = 'luiz'

from flask_restful import abort as rest_abort, wraps
from flask_restful import request
from taxi_api.business.user_session import UserSessionBus
from helpers import Helpers


class ApiAuth(object):

    _cfg = Helpers.load_config()
    _ds_name = _cfg["api"]["database"]
    _environ = _cfg["env"]
    _session_bus = UserSessionBus(_ds_name, _environ)

    def __init__(self, *args, **kwargs):
        self.role = kwargs.get("role")

    def login_required(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if self._validate_token():
                return func(*args, **kwargs)
            rest_abort(401)
        return wrapper

    def _validate_token(self):
        api_token = request.environ.get('HTTP_API_TOKEN')
        if not api_token:
            return
        user_to = ApiAuth._session_bus.get_user_from_session(api_token)
        if not user_to or (self.role and user_to.role != self.role):
            return
        return user_to
