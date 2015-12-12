__author__ = 'luiz'

from base import TO
import fields
from hashlib import md5


class UserTO(TO):

    user_id = fields.StringField(pk=1)
    email = fields.StringField()
    password = fields.StringField()
    name = fields.StringField()
    role = fields.StringField(options=["driver", "passenger"])
    car_plate = fields.StringField(null=True)

    def _before_serialize(self):
        self.user_id = md5(self.email).hexdigest()
        if self.password:
            self.password = md5(self.password).hexdigest()
        car_plate_needed = self.role == "driver"
        if car_plate_needed and not self.car_plate:
            raise ValueError("Car plate is required for role driver")
