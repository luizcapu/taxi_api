__author__ = 'luiz'

from base import DBBaseDao
from taxi_api.to.user_session import UserSessionTO
from taxi_api.dao.elasticsearch.user import UserDao


class UserSessionDao(DBBaseDao):
    _default_table = "user_session"
    _to_class = UserSessionTO
    _user_dao = None

    def _get_user_dao(self):
        if UserSessionDao._user_dao is None:
            UserSessionDao._user_dao = UserDao(self.ds_provider, self.data_source)
        return UserSessionDao._user_dao

    def get_user_from_session(self, api_token, **kwargs):
        for session_to in self.search_by_field_value("api_token", api_token, **kwargs):
            user_to = self._get_user_dao().get_by_pk(session_to.user_id)
            if user_to:
                user_to.password = "_"
                return user_to
            return

    def logout(self, api_token, **kwargs):
        user_to = self.get_user_from_session(api_token)
        if user_to:
            self.delete(self.get_by_pk(user_to.user_id))
