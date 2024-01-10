from app.model.todo import Todos as Todo
from flask import request, jsonify
from app import response, db
from app.controller import UserController
from flask_jwt_extended import *

@jwt_required()
def index():
    try:
        user_id = request.args.get('user_id')
        todos = Todo.query.filter_by(user_id=user_id).all()
        data = transform(todos)
        return response.ok(data, "")
    except Exception as e:
        print(e)

def store():
    try:
        todo = request.json['todo']
        desc = request.json['description']
        user_id = request.json['user_id']
        new_todo = Todo(user_id=user_id, todo=todo, description=desc)
        db.session.add(new_todo)
        db.session.commit()
        return response.ok('', 'Successfully create todo!')
    except Exception as e:
        print(e)

def update(id):
    try:
        todo = request.json['todo']
        desc = request.json['description']
        todo_to_update = Todo.query.filter_by(id=id).first()
        todo_to_update.todo = todo
        todo_to_update.description = desc
        db.session.commit()
        return response.ok('', 'Successfully update todo!')
    except Exception as e:
        print(e)

def show(id):
    try:
        todo = Todo.query.filter_by(id=id).first()
        if not todo:
            return response.badRequest([], 'Empty....')
        data = singleTransform(todo)
        return response.ok(data, "")
    except Exception as e:
        print(e)

def delete(id):
    try:
        todo_to_delete = Todo.query.filter_by(id=id).first()
        if not todo_to_delete:
            return response.badRequest([], 'Empty....')
        db.session.delete(todo_to_delete)
        db.session.commit()
        return response.ok('', 'Successfully delete data!')
    except Exception as e:
        print(e)

def transform(values):
    array = []
    for i in values:
        array.append(singleTransform(i))
    return array

def singleTransform(values):
    data = {
        'id': values.id,
        'user id': values.user_id,
        'todo': values.todo,
        'description': values.description,
        'created_at': values.created_at,
        'updated_at': values.updated_at,
        'user': UserController.singleTransform(values.users, withTodo=False)
    }
    return data
