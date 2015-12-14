#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'luiz'

import os
import argparse

from flask import Flask
from flask.ext.restful import Api
from flask_restful_swagger import swagger

from helpers.helpers import Helpers
from taxi_api.init_db import run_main as run_init_db


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-e", "--env", type=str, default="test",
                        help="Environment to run (prod|test). Default: test")
    args = parser.parse_args()
    os.environ["api_env"] = args.env

    if not os.environ.get("db_loaded", None):
        run_init_db()
        os.environ["db_loaded"] = "y"

    cfg = Helpers.load_config()
    api_cfg = cfg["api"]

    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True
    api = swagger.docs(Api(app),
                       apiVersion=api_cfg["version"],
                       basePath='http://127.0.0.1:%i' % api_cfg["port"],
                       resourcePath='/',
                       produces=["application/json", "text/html"],
                       api_spec_url='/api/spec',
                       description='99taxis API Project')

    import resources  # import resources after configure environment
    _resources = [
        resources.Driver, resources.DriverInArea, resources.UserCreate,
        resources.UserLogin, resources.UserLogout, resources.RequestDriver,
        resources.RequestHistory]

    for _res in _resources:
        _res.register(api)

    app.run(debug=cfg["env"] != "prod", host=api_cfg["host"], port=api_cfg["port"])

