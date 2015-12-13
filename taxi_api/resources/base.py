__author__ = 'luiz'

from flask_restful import Resource
from taxi_api.helpers.helpers import Helpers
from taxi_api.helpers.api_auth import ApiAuth
import traceback

class BaseResource(Resource):

    _cfg = Helpers.load_config()
    _ds_name = _cfg["api"]["database"]
    _environ = _cfg["env"]

    _driver_auth = ApiAuth(role="driver")
    _passenger_auth = ApiAuth(role="passenger")
    _user_auth = ApiAuth()

    @staticmethod
    def register(api):
        pass

    def return_exception(self, e, code):
        print e
        return self.return_message(e.message or e.args[1], code)

    def return_message(self, msg, code):
        return {"message": msg}, code
