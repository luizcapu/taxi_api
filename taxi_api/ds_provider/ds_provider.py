__author__ = 'luiz'

from collections import namedtuple
from ..helpers.helpers import Helpers
import os


class DSProvider(object):

    __instance = None

    _DS_PATH = "%s/datasources" % os.path.dirname(__file__)
    _INTERFACE = "ds_interface.DSInterface"

    DRIVERS = namedtuple("DRIVERS", "elasticsearch")
    _ENABLED_DRIVERS = DRIVERS("elasticsearch")
    _DRIVER_CLASSES = DRIVERS("ds_elasticsearch.DSElasticSearch")

    def __init__(self):
        assert DSProvider.__instance is None, "Please use DSProvider.get() to get a singleton instead"
        self.data_sources = {}

    @staticmethod
    def get():
        if DSProvider.__instance is None:
            DSProvider.__instance = DSProvider()
        return DSProvider.__instance

    def get_data_source(self, ds_name, environment, connect_now=True, do_validate=True):
        ds_key = (ds_name, environment)
        if ds_key in self.data_sources:
            if do_validate:
                self.data_sources[ds_key].validate()
        else:
            if ds_name not in DSProvider._ENABLED_DRIVERS._asdict():
                raise ValueError("Enabled type %s. Enabled types are %s" % (ds_name, str(DSProvider.DRIVERS)))

            config = Helpers.load_ds_config(environment=environment)

            driver_class = DSProvider._DRIVER_CLASSES._asdict().get(ds_name)
            data_source = DSProvider._create_data_source(driver_class, ds_name, environment, config)
            if connect_now:
                data_source.connect()
            self.data_sources[ds_key] = data_source

        return self.data_sources[ds_key]

    @staticmethod
    def _create_data_source(driver_class, ds_name, environment, config):
        base_ds_class = DSProvider._get_class(DSProvider._INTERFACE)
        ds_class = DSProvider._get_class(driver_class)
        if not issubclass(ds_class, base_ds_class):
            raise Exception("Could not instantiate '%s', class should inherit from %s" %
                            (driver_class, DSProvider._INTERFACE))
        return ds_class(ds_name, environment, config)

    @staticmethod
    def _get_class(datasource):
        module_name, clazz = datasource.split(".")
        return Helpers.get_class_from_file("%s/%s.py" % (DSProvider._DS_PATH, module_name), module_name, clazz)


