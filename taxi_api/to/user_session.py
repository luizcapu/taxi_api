__author__ = 'luiz'

from base import TO
import fields


class UserSessionTO(TO):

    user_id = fields.StringField(pk=1)
    api_token = fields.StringField()
