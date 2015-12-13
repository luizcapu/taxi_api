__author__ = 'luiz'

import json
from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.request_driver import RequestDriverBus
from taxi_api.to.request_driver import RequestDriverTO
from flask_restful import reqparse, request
from taxi_api.helpers.exceptions import UserHasActiveRequest

parser = reqparse.RequestParser()
parser.add_argument('location', required=True, type=str, help='JSON string representing geo point location of requester (must have "lat" and "lon" keys)')


class RequestDriver(BaseResource):
    _request_driver_bus = RequestDriverBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='get_user_active_request',
        notes="Get current user's active request",
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
                "code": 201,
                "message": "No active requests found."
            },
            {
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    @BaseResource._user_auth.login_required
    def get(self):
        try:
            active_requests = list(
                RequestDriver._request_driver_bus.list_active_per_user(
                    request.current_user.user_id))
            if active_requests:
                return [
                    r.serialize()
                    for r in
                    active_requests
                ]
            else:
                return self.return_message("No active requests found", 201)
        except Exception as e:
            return self.return_exception(e, 500)

    @swagger.operation(
        nickname='create_driver_request',
        notes='Create a new driver request for current logged user',
        parameters=[
            {
                "name": "location",
                "description": 'JSON string representing geo point location of requester (must have "lat" and "lon" keys). Geo point must have "lat" and "lon" keys. i.e.: {"lat":40.730, "lon":-73.989}',
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "query"
            },
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
                "code": 201,
                "message": "User already has an active request."
            },
            {
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    @BaseResource._user_auth.login_required
    def put(self):
        try:
            args = parser.parse_args()
            location = json.loads(args.location)

            to_obj = RequestDriverTO(**(dict(
                requester_id=request.current_user.user_id,
                requester_location=location,
                status="active"
            )))

            # call update_if_exists to ensure its a driver
            RequestDriver._request_driver_bus.create_request(to_obj)
        except UserHasActiveRequest:
            return self.return_message("User already has an active request", 201)
        except Exception as e:
            return self.return_exception(e, 500)

    @swagger.operation(
        nickname='cancel_driver_request',
        notes='Cancel a driver request',
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
            RequestDriver._request_driver_bus.cancel_active_requests(request.current_user.user_id)
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(RequestDriver, '/user/driver_request', endpoint="request_driver")
