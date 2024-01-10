from app import app
from app.controller import UserController
from app.controller import TodoController
from flask import request

@app.route('/login', methods=['POST'])
def login():
    return UserController.login()

@app.route('/refresh', methods=['POST'])
def refresh():
    return UserController.refresh()

@app.route('/users', methods=['POST', 'GET'])
def users():
    if request.method == 'GET':
        return UserController.index()
    else:
        return UserController.store()

@app.route('/users/<id>', methods=['GET', 'PUT', 'DELETE'])
def usersDetail(id):
    if request.method == 'GET':
        return UserController.show(id)
    elif request.method == 'PUT':
        return UserController.update(id)
    elif request.method == 'DELETE':
        return UserController.delete(id)


@app.route('/todo', methods=['POST', 'GET'])
def todo():
    if request.method == 'GET':
        return TodoController.index()
    else:
        return TodoController.store()

@app.route('/todo/<id>', methods=['PUT', 'GET', 'DELETE'])
def todoDetail(id):
    if request.method == 'GET':
        return TodoController.show(id)
    elif request.method == 'PUT':
        return TodoController.update(id)
    elif request.method == 'DELETE':
        return TodoController.delete(id)

