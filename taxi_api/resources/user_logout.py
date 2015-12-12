__author__ = 'luiz'

import json
from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.user_session import UserSessionBus
from flask_restful import request


class UserLogout(BaseResource):
    _user_session_bus = UserSessionBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='user_logout',
        notes='Logout user from platform',
        parameters=[
            {
                "name": "api_token",
                "description": "API access token",
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
    @BaseResource._user_auth.login_required
    def post(self):
        try:
            UserLogout._user_session_bus.logout(request.environ.get('HTTP_API_TOKEN'))
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(UserLogout, '/user/logout', endpoint="user_logout")
