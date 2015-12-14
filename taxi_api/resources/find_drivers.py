__author__ = 'luiz'

import json
from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.driver import DriverBus
from flask_restful import reqparse
from taxi_api.helpers.driver_finder import DriverFinder

parser = reqparse.RequestParser()
parser.add_argument('location', required=True, type=str, help='JSON string representing geo point location of requester (must have "lat" and "lon" keys)')
parser.add_argument('desired_drivers', required=True, type=int, help='Number of desired drivers to retrieve')


class FindDrivers(BaseResource):
    _finder = DriverFinder()

    @swagger.operation(
        nickname='driver_in_area',
        notes='Retrieve a list of available drivers in a given geo rectangle (nw/se geo points). Geo point must have "lat" and "lon" keys. i.e.: {"lat":40.730, "lon":-73.989}',
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
                "name": "desired_drivers",
                "description": 'Number of desired drivers to retrieve',
                "required": True,
                "allowMultiple": False,
                "dataType": "integer",
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
    @BaseResource._user_auth.login_required
    def get(self):
        try:
            args = parser.parse_args()
            return [
                driver.serialize()
                for driver in
                FindDrivers._finder.run(json.loads(args.location), args.desired_drivers)
            ]
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(FindDrivers, '/drivers/findFromLocation', endpoint="find_drivers")
