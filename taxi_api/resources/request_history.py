__author__ = 'luiz'

from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.request_driver import RequestDriverBus
from flask_restful import request


class RequestHistory(BaseResource):
    _request_driver_bus = RequestDriverBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='list_user_driver_requests',
        notes='List all driver requests of the user',
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
    def get(self):
        try:
            return [
                r.serialize()
                for r in
                RequestHistory._request_driver_bus.search_by_field_value(
                    "requester_id", request.current_user.user_id)
            ]
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(RequestHistory, '/user/requests_history', endpoint="user_requests_history")
