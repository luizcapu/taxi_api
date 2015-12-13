__author__ = 'luiz'

from base import DBBaseDao
from taxi_api.to.request_driver import RequestDriverTO


class RequestDriverDao(DBBaseDao):
    _default_table = "request_driver"
    _to_class = RequestDriverTO
