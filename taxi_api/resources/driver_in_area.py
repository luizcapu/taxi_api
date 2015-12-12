__author__ = 'luiz'

import json
from flask_restful_swagger import swagger
from base import BaseResource
from taxi_api.business.driver import DriverBus
from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('nw', required=True, type=str, help='JSON string representing extreme north/west of rectangle (must have "lat" and "lon" keys)')
parser.add_argument('se', required=True, type=str, help='JSON string representing extreme south/east of rectangle (must have "lat" and "lon" keys)')


class DriverInArea(BaseResource):
    _driver_bus = DriverBus(BaseResource._ds_name, BaseResource._environ)

    @swagger.operation(
        nickname='driver_in_area',
        notes='Retrieve a list of available drivers in a given geo rectangle (nw/se geo points). Geo point must have "lat" and "lon" keys. i.e.: {"lat":40.730, "lon":-73.989}',
        parameters=[
            {
                "name": "nw",
                "description": 'JSON string representing extreme north/west of rectangle (must have "lat" and "lon" keys)',
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "query"
            },
            {
                "name": "se",
                "description": 'JSON string representing extreme south/esat of rectangle (must have "lat" and "lon" keys)',
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
    @BaseResource._user_auth.login_required
    def get(self):
        try:
            args = parser.parse_args()
            nw = json.loads(args["nw"])
            se = json.loads(args["se"])
            return [driver.serialize() for driver in DriverInArea._driver_bus.list_in_rectangle(nw, se)]
        except Exception as e:
            return self.return_exception(e, 500)

    @staticmethod
    def register(api):
        api.add_resource(DriverInArea, '/drivers/inArea', endpoint="drivers")
