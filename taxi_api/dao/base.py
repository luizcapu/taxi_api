from abc import ABCMeta, abstractmethod

__author__ = 'luiz'


class BaseDao(object):
    __metaclass__ = ABCMeta
    _UNDEFINED_TABLE = "undefined:set"
    _default_table = _UNDEFINED_TABLE
    _to_class = None

    def __init__(self, ds_provider, data_source):
        self.ds_provider = ds_provider
        self.data_source = data_source

    @abstractmethod
    def _record_to_to(self, record):
        pass

    @abstractmethod
    def save(self, to_obj, **kwargs):
        pass

    @abstractmethod
    def update_if_exists(self, to_obj, **args):
        pass

    @abstractmethod
    def save_if_up_to_date(self, to_obj, **kwargs):
        pass

    @abstractmethod
    def create(self, to_obj, **kwargs):
        pass

    @abstractmethod
    def get_by_pk(self, pk, *fields, **kwargs):
        pass

    @abstractmethod
    def get_by_pks(self, pks, *fields, **kwargs):
        pass

    @abstractmethod
    def search_by_field_value(self, field_to_search, value_to_search, *fields, **kwargs):
        pass

    @abstractmethod
    def search_by_field_range(self, field_to_search, initial_range, final_range, *fields, **kwargs):
        pass

    @abstractmethod
    def create_db(self, **kwargs):
        pass

    @abstractmethod
    def create_table(self, **kwargs):
        pass
