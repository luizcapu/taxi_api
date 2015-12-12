__author__ = 'luiz'

from flask import Flask
from flask.ext.restful import Api
from flask_restful_swagger import swagger
import resources
from helpers.helpers import Helpers
from init_db import run_main as run_init_db
import os


if __name__ == '__main__':

    if not os.environ.get("db_loaded", None):
        run_init_db()
        os.environ["db_loaded"] = "y"

    cfg = Helpers.load_config()
    api_cfg = cfg["api"]

    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True
    api = swagger.docs(Api(app),
                       apiVersion=api_cfg["version"],
                       basePath='http://%s:%s' % (api_cfg["host"], api_cfg["port"]),
                       resourcePath='/',
                       produces=["application/json", "text/html"],
                       api_spec_url='/api/spec',
                       description='99taxis API Project')

    _resources = [
        resources.Driver, resources.DriverInArea, resources.UserCreate,
        resources.UserLogin, resources.UserLogout]

    for _res in _resources:
        _res.register(api)

    app.run(debug=cfg["env"] != "prod")

