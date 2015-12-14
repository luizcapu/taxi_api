__author__ = 'luiz'

from base import BaseBus
from taxi_api.helpers.helpers import Helpers


class DriverBus(BaseBus):
    _ref = "driver"

    def list_in_rectangle(self, top_left, bottom_right, only_active=True,
                          top_left_exclude=None, bottom_right_exclude=None):
        return self.dao.list_in_rectangle(
            Helpers.validate_geo_point(top_left),
            Helpers.validate_geo_point(bottom_right),
            only_active,
            top_left_exclude, bottom_right_exclude
        )
