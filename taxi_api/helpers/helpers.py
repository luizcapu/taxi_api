__author__ = 'luiz'

import os
import json
import sys
import imp
from taxi_api.to.fields import GeoPointField


class Helpers(object):

    _loaded_configs = {}

    @staticmethod
    def get_class(kls):
        parts = kls.split('.')
        module = ".".join(parts[:-1])
        #m = importlib.import_module(module, kls)
        m = __import__(module)
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    @staticmethod
    def get_class_from_file(file, module_name, kls):
        with open(file, "r") as f:
            module = imp.new_module(module_name)
            exec str(f.read()) in module.__dict__
            sys.modules[module_name] = module
        m = __import__(module_name)
        return m.__getattribute__(kls)

    @staticmethod
    def concat(args, glue=":"):
        if not isinstance(args, (tuple, list)):
            raise Exception("args must be list or tuple")
        return glue.join(str(arg) for arg in args)

    @staticmethod
    def load_config(environment=None, force_reload=False):
        if environment is None:
            print "env is None, getting from os.environ"
            environment = os.environ.get("api_env", "test")
            print "env=", environment
        if not environment in Helpers._loaded_configs.keys() or force_reload:
            # get location of cfg file
            base_path = os.path.abspath(os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir))
            cfg_file = "%s/config/cfg-%s.json" % (base_path, environment)

            # read cfg file
            with open(cfg_file, "r+") as f:
                cfg = json.loads(f.read())
                cfg["env"] = environment
                Helpers._loaded_configs[environment] = cfg

        return Helpers._loaded_configs[environment]

    @staticmethod
    def load_ds_config(environment=None, force_reload=False):
        cfg = Helpers.load_config(environment, force_reload)
        return cfg["datasources"][cfg["api"]["database"]]


    @staticmethod
    def dispatch(service, message):
        # TODO implement real dispatch. For now it just print emulating a dispatch to another service
        print "Will dispatch message %s to service %s" % (message, service)

    @staticmethod
    def file_name_to_class_name(file_name):
        must_upper = True
        result = ""
        for letter in file_name:
            if letter == "_":
                must_upper = True
            else:
                result += letter.upper() if must_upper else letter
                must_upper = False
        return result

    @staticmethod
    def validate_geo_point(geo_point):
        geo_field = GeoPointField()
        geo_field.validate(geo_point)
        return geo_field.serialize(geo_point)