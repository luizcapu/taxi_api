__author__ = 'luiz'

from base import BaseBus


class UserSessionBus(BaseBus):
    _ref = "user_session"

    def get_user_from_session(self, api_token, **kwargs):
        return self.dao.get_user_from_session(api_token, **kwargs)

    def logout(self, api_token, **kwargs):
        return self.dao.logout(api_token, **kwargs)