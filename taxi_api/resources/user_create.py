__author__ = 'luiz'

import json
from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.user import UserBus
from flask_restful import reqparse, request

parser = reqparse.RequestParser()
parser.add_argument('user', required=True, type=str, help='JSON string representation of user')


class UserCreate(BaseResource):
    _user_bus = UserBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='user_create',
        notes='Create a new user in platform',
        parameters=[
            {
                "name": "app_access_key",
                "description": 'Client app access key to consume user creation (Please, use default key "test_key")',
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "header"
            },
            {
                "name": "user",
                "description": 'JSON string representation of user. i.e: {"name": "Luiz", "car_plate": "ABC-1234", "role": "driver", "password": "my_pass", "email": "luizcapu@gmail.com"}',
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "query"
            }
        ],
        responseMessages=[
            {
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    @BaseResource._user_auth.app_key_required
    def post(self):
        try:
            args = parser.parse_args()
            user = json.loads(args.user)
            UserCreate._user_bus.create(user)
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(UserCreate, '/user/create', endpoint="user_create")
