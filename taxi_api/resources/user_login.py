__author__ = 'luiz'

from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.user import UserBus
from flask_restful import request


class UserLogin(BaseResource):
    _user_bus = UserBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='user_login',
        notes='Login user in platform',
        parameters=[
            {
                "name": "username",
                "description": 'User email',
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "password",
                "description": 'User password',
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            }
        ],
        responseMessages=[
            {
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    def post(self):
        try:
            login_result = UserLogin._user_bus.login(
                request.environ.get('HTTP_USERNAME'),
                request.environ.get('HTTP_PASSWORD')
            )
            if login_result:
                user_to, api_token = login_result
                usr_response = user_to.serialize()
                usr_response.pop("password")
                return usr_response, 200, {'api_token': api_token}
            else:
                raise Exception("Invalid login")
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(UserLogin, '/user/login', endpoint="user_login")
