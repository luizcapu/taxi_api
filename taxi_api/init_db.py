# coding: utf-8
__author__ = 'luiz'

from taxi_api.helpers.helpers import Helpers
from taxi_api.ds_provider.ds_provider import DSProvider
import os


def run_main():
    cfg = Helpers.load_config()
    db_cfg = Helpers.load_ds_config()

    ds_provider = DSProvider.get()
    datasource = ds_provider.get_data_source(cfg["api"]["database"], cfg["env"])

    # load database class and create database
    db_file = "dao.%s.base.DBBaseDao" % cfg["api"]["database"]
    db_loader = Helpers.get_class(db_file)(ds_provider, datasource)
    print "Creating database"
    db_loader.create_db(**db_cfg)

    # parse dao files and create tables
    cur_dir = os.path.dirname(os.path.realpath(__file__))
    if not isinstance(cur_dir, unicode):
        cur_dir = cur_dir.decode("utf-8")
    _dao_path = cur_dir + "/dao/" + cfg["api"]["database"]
    _ignore_in_load = ["__init__.py", "base.py", "init_db.py"]
    for file_in_dir in os.listdir(_dao_path):
        if file_in_dir.endswith(".py") and not file_in_dir in _ignore_in_load:
            module_name = file_in_dir[:-3]
            dao_class_name = Helpers.file_name_to_class_name(module_name) + "Dao"
            print "Creating table for %s" % dao_class_name
            clazz = Helpers.get_class(
                "dao.%s.%s.%s" % (cfg["api"]["database"], module_name, dao_class_name))
            dao_obj = clazz(ds_provider, datasource)
            dao_obj.create_table(**db_cfg)
    print "Database created !"

if __name__ == '__main__':
    run_main()