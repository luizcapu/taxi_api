__author__ = 'luiz'

from flask import Flask
from flask.ext.restful import Api
from flask_restful_swagger import swagger
import resources


if __name__ == '__main__':

    app = Flask(__name__)
    app.config['BUNDLE_ERRORS'] = True
    api = swagger.docs(Api(app),
                       apiVersion='0.1',
                       basePath='http://localhost:5000',
                       resourcePath='/',
                       produces=["application/json", "text/html"],
                       api_spec_url='/api/spec',
                       description='99taxis API Project')

    _resources = [resources.Driver, resources.DriverInArea]

    for _res in _resources:
        _res.register(api)

    app.run(debug=True)

