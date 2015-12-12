__author__ = 'luiz'

from base import DBBaseDao
from taxi_api.to.user import UserTO
from taxi_api.to.driver import DriverTO
from taxi_api.dao.elasticsearch.driver import DriverDao


class UserDao(DBBaseDao):
    _default_table = "user"
    _to_class = UserTO

    def create(self, to_obj, **args):
        super(UserDao, self).create(to_obj, **args)

        if to_obj.role == "driver":
            # post initial status for driver
            # enabling future update_if_exists
            driver_dao = DriverDao(self.ds_provider, self.data_source)
            driver_to = DriverTO(driver_id=to_obj.user_id, available=True, location=(0, 0))
            driver_dao.save(driver_to)
