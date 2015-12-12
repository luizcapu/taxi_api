__author__ = 'luiz'

from base import BaseBus


class UserBus(BaseBus):
    _ref = "user"

    def login(self, username, password, **kwargs):
        return self.dao.login(username, password, **kwargs)