__author__ = 'luiz'

from base import PKUUIDTO
import fields
from datetime import datetime


class RequestDriverTO(PKUUIDTO):
    requester_id = fields.StringField()
    requester_location = fields.GeoPointField()
    driver_id = fields.StringField(null=True, store_null=False)
    status = fields.StringField(options=["active", "canceled", "finished"])
    created_in = fields.DateTimeField(default=datetime.now)
