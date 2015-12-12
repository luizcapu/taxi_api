__author__ = 'luiz'

from base import TO
import fields
from hashlib import md5


class UserTO(TO):

    user_id = fields.StringField(pk=1)
    email = fields.StringField()
    password = fields.StringField()
    name = fields.StringField()
    role = fields.StringField()

    def _before_serialize(self):
        self.user_id = md5(self.email).hexdigest()
        print "a"


u = UserTO(**dict(email="luizcapu@gmail.com", password="123", name="Luiz", role="driver"))

print u.serialize()