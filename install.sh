#!/bin/sh

rm -fr build
pip install flask-restful
pip install flask-restful-swagger
pip install 'elasticsearch>=2.0.0'
python setup.py install


