__author__ = 'luiz'

from base import TO
import fields
from datetime import datetime
from uuid import uuid4


class RequestDriverTO(TO):
    request_id = fields.StringField(pk=1, default=uuid4, default_cast=str)
    requester_id = fields.StringField()
    requester_location = fields.GeoPointField()
    driver_id = fields.StringField(null=True, store_null=False)
    status = fields.StringField(options=["active", "canceled", "finished"])
    created_in = fields.DateTimeField(default=datetime.now)
