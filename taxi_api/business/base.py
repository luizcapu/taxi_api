__author__ = 'luiz'

from ..ds_provider.ds_provider import DSProvider
from itertools import chain
from ..helpers.helpers import Helpers


class BaseBus(object):

    _ref = "base_service"
    _DAO_PATH = "taxi_api.dao"
    _TO_PATH = "taxi_api.to"

    def __init__(self, ds_name, environment):
        self.ds_provider = DSProvider.get()
        self.data_source = self.ds_provider.get_data_source(ds_name=ds_name, environment=environment, do_validate=False)

        self.dao_type = ds_name
        self.dao_class_name = "%s.%s.%s.%sDao" % (self._DAO_PATH, self.dao_type, self._ref, self.__class__.__name__[:-3])
        self.dao_class = Helpers.get_class(self.dao_class_name)
        self.dao = self.dao_class(self.ds_provider, self.data_source)
        self.ds_name = ds_name
        self.ds_environment = environment

        self.to_class_name = "%s.%s.%sTO" % (self._TO_PATH, self._ref, self.__class__.__name__[:-3])
        self.to_class = Helpers.get_class(self.to_class_name)

    def exists(self, pk, **args):
        return self.dao.exists(pk, **args)

    # Write the record, regardless of existence. (i.e. create or update.)
    def save(self, to_obj, **args):
        if isinstance(to_obj, dict):
            to_obj = self.to_class(**to_obj)

        return self.dao.save(to_obj, **args)

    # Write the record, ONLY if it exists.
    def update_if_exists(self, to_obj, **args):
        if isinstance(to_obj, dict):
            to_obj = self.to_class(**to_obj)

        return self.dao.update_if_exists(to_obj, **args)

    # Create a record, ONLY if it doesn't exist.
    def create(self, to_obj, **args):
        if isinstance(to_obj, dict):
            to_obj = self.to_class(**to_obj)

        return self.dao.create(to_obj, **args)

    # Returns a tuple of (object, created), where object is the retrieved or created
    # and created is a boolean specifying whether a new object was created.
    def create_or_get(self, to_obj, **args):
        if isinstance(to_obj, dict):
            to_obj = self.to_class(**to_obj)

        if self.dao.create(to_obj, **args):
            return to_obj, True
        return self.get_by_pk(to_obj.pk), False

    def replace(self, to_obj, **args):
        if isinstance(to_obj, dict):
            to_obj = self.to_class(**to_obj)
        return self.dao.replace(to_obj, **args)

    def delete(self, to_obj, **args):
        return self.dao.delete(to_obj, **args)

    def search_by_field_value(self, field_to_search, value_to_search, *fields, **args):
        if isinstance(field_to_search, list) and isinstance(value_to_search, list):
            for i in xrange(0, len(field_to_search)):
                search_field = self.to_class.get_field(field_to_search[i])
                search_field.validate(value_to_search[i])
                value_to_search[i] = search_field.serialize(value_to_search[i])
        else:
            search_field = self.to_class.get_field(field_to_search)
            search_field.validate(value_to_search)
            value_to_search = search_field.serialize(value_to_search)
        return self.dao.search_by_field_value(field_to_search, value_to_search, *fields, **args)

    def search_by_field_range(self, field_to_search, initial_range, final_range, *fields, **args):
        search_field = self.to_class.get_field(field_to_search)
        search_field.validate(initial_range)
        search_field.validate(final_range)
        initial_range = search_field.serialize(initial_range)
        final_range = search_field.serialize(final_range)
        return self.dao.search_by_field_range(field_to_search, initial_range, final_range, *fields, **args)

    def search_by_field_range_steps(self, field_to_search, initial_range, final_range, step, inner_range,
                                    *fields, **args):
        def iterate():
            _start = initial_range
            while _start <= final_range:
                _end = _start + inner_range
                if _end > final_range:
                    _end = final_range

                yield self.search_by_field_range(field_to_search, _start, _end, *fields, **args)

                _start += step

        return chain.from_iterable(iterate())

    def save_if_up_to_date(self, to_obj, **kwargs):
        if isinstance(to_obj, dict):
            to_obj = self.to_class(**to_obj)
        return self.dao.save_if_up_to_date(to_obj, **kwargs)

    def search_by_field_value_range(self, field_to_search, value, initial_range, final_range, step, *fields, **args):
        def iterate():
            _start = initial_range
            while _start <= final_range:
                value_to_search = Helpers.concat([value, _start])
                yield self.search_by_field_value(field_to_search, value_to_search, *fields, **args)
                _start += step

        return chain.from_iterable(iterate())

    def get_by_pk(self, pk, *fields, **args):
        return self.dao.get_by_pk(pk, *fields, **args)

    def get_by_pks(self, pks, *fields, **args):
        return self.dao.get_by_pks(pks, *fields, **args)

    def get_all(self, **kwargs):
        return self.dao.get_all(**kwargs)
