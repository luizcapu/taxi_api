__author__ = 'luiz'

from base import TO
import fields


class DriverTO(TO):

    driver_id = fields.StringField(pk=1)
    location = fields.GeoPointField()
    available = fields.BooleanField()

