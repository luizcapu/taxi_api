__author__ = 'luiz'

import json
from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.driver import DriverBus
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('status', required=True, type=str, help='JSON string representation of driver status')


class Driver(BaseResource):
    _driver_bus = DriverBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        notes='Retrieve driver status for a given driver_id',
        responseMessages=[
            {
                "code": 201,
                "message": "Driver not found"
            },
            {
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    def get(self, driver_id):
        try:
            driver_to = Driver._driver_bus.get_by_pk(driver_id)

            if driver_to:
                return driver_to.serialize()
            else:
                return self.return_message("Driver %i not found" % driver_id, 201)
        except Exception as e:
            return self.return_exception(e, 500)

    @swagger.operation(
        notes='Save driver status',
        parameters=[
            {
                "name": "status",
                "description": "JSON string representation of driver status",
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
                "code": 500,
                "message": "Exception during execution"
            }
        ]
    )
    def post(self, driver_id):
        try:
            args = parser.parse_args()
            status = json.loads(args.status)
            status["driver_id"] = driver_id
            Driver._driver_bus.save(status)
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(Driver, '/driver/<int:driver_id>/status', endpoint="driver")
