__author__ = 'luiz'

from flask import request
from flask_restful import Resource
from flask_restful_swagger import swagger
from base import BaseResource

todos = {}
class TodoSimple(BaseResource):

    @swagger.operation(
        notes='some really good notes',
        responseClass="AAAAA",
        nickname='upload',
        parameters=[
            {
              "name": "body",
              "description": "blueprint object that needs to be added. YAML.",
              "required": True,
              "allowMultiple": False,
              "dataType": "BBBBB",
              "paramType": "body"
            }
          ],
        responseMessages=[
            {
              "code": 201,
              "message": "Created. The URL of the created blueprint should be in the Location header"
            },
            {
              "code": 405,
              "message": "Invalid input"
            }
          ]
        )
    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        return {todo_id: todos[todo_id]}

    @staticmethod
    def register(api):
        api.add_resource(TodoSimple, '/task/<string:todo_id>')
