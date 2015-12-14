__author__ = 'luiz'

from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.request_driver import RequestDriverBus
from flask_restful import reqparse, request
from taxi_api.helpers.exceptions import OutDatedRecordException

parser = reqparse.RequestParser()
parser.add_argument('request_id', required=True, type=str, help='Request ID to assign driver')


class RequestAssignment(BaseResource):
    _request_driver_bus = RequestDriverBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='get_driver_active_request',
        notes="Get current driver's active request",
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
    @BaseResource._driver_auth.login_required
    def get(self):
        try:
            active_requests = list(
                RequestAssignment._request_driver_bus.list_active_per_driver(
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
        nickname='assign_driver_to_request',
        notes='Assign a driver ID to meet the request',
        parameters=[
            {
                "name": "request_id",
                "description": "Request ID to assign driver",
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
                "message": "Request is no longer available"
            },
            {
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    @BaseResource._driver_auth.login_required
    def post(self):
        try:
            args = parser.parse_args()
            try:
                RequestAssignment._request_driver_bus.assign_driver(args.request_id, request.current_user.user_id)
            except OutDatedRecordException as e:
                return self.return_message("Request is no longer available", 201)
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(RequestAssignment, '/driver/request_assignment', endpoint="driver_request_assignment")
