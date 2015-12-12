__author__ = 'luiz'

from base import DBBaseDao
from taxi_api.to.user import UserTO
from taxi_api.to.driver import DriverTO
from taxi_api.dao.elasticsearch.driver import DriverDao
from hashlib import md5
from uuid import uuid4


class UserDao(DBBaseDao):
    _default_table = "user"
    _to_class = UserTO
    _driver_dao = None
    _user_session_dao = None

    def _get_driver_dao(self):
        if UserDao._driver_dao is None:
            UserDao._driver_dao = DriverDao(self.ds_provider, self.data_source)
        return UserDao._driver_dao

    def _get_user_session_dao(self):
        if UserDao._user_session_dao is None:
            from taxi_api.dao.elasticsearch.user_session import UserSessionDao
            UserDao._user_session_dao = UserSessionDao(self.ds_provider, self.data_source)
        return UserDao._user_session_dao

    def create(self, to_obj, **args):
        super(UserDao, self).create(to_obj, **args)

        if to_obj.role == "driver":
            # post initial status for driver
            # enabling future update_if_exists
            driver_to = DriverTO(driver_id=to_obj.user_id, available=True, location=(0, 0))
            self._get_driver_dao().save(driver_to)

    def login(self, username, password, **kwargs):
        user_to = self.get_by_pk(md5(username).hexdigest())
        if user_to and user_to.password == md5(password).hexdigest():
            api_token = md5(str(uuid4)).hexdigest()
            self._get_user_session_dao().save(
                self._get_user_session_dao()._to_class(
                    **dict(api_token=api_token, user_id=user_to.user_id))
            )
            return user_to, api_token
