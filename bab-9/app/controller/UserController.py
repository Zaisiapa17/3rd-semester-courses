from app.model.user import Users
from app import response, app, db
from datetime import datetime, timedelta
from flask import request
from flask_jwt_extended import create_access_token, create_refresh_token
from flask_jwt_extended import *


@jwt_required(refresh=True)
def refresh():
    try:
        user = get_jwt_identity()
        new_token = create_access_token(identity=user, fresh=False)

        return response.ok({'token_access': new_token}, "success!")
    except Exception as error:
        print(f'Failed to connect: {error}')

def login():
    try:
        email = request.json.get('email')
        password = request.json.get('password')

        if not email or not password:
            return response.badRequest([], 'Email and password are required.')

        user = Users.query.filter_by(email=email).first()

        if not user:
            return response.badRequest([], 'User not found.')

        if not user.checkPassword(password):
            return response.badRequest([], 'Invalid credentials.')

        data = singleTransform(user, withTodo=False)
        expires = timedelta(days=1)
        expires_refresh = timedelta(days=3)
        access_token = create_access_token(data, fresh=True, expires_delta=expires)
        refresh_token = create_refresh_token(data, expires_delta=expires_refresh)
        return response.ok({'data': data, 'token_access': access_token, 'token_refresh': refresh_token}, "Login successful")

    except Exception as e:
        print(e)


def index():
    try:
        users = Users.query.all()
        data = transform(users)
        return response.ok(data, "")
    except Exception as e:
        print(e)

def transform(users):
    array = []
    for i in users:
        array.append({
            'id': i.id,
            'name': i.name,
            'email': i.email,
        })
    return array

def show(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], 'Empty....')
        
        data = singleTransform(user)
        return response.ok(data, "")
    except Exception as e:
        print(e)

def singleTransform(users, withTodo=True):
    data = {
        'id': users.id,
        'name': users.name,
        'email': users.email
    }

    if withTodo:
        todos = []
        for i in users.todos:
            todos.append({
                'id': i.id,
                'todo': i.todo,
                'description': i.description
            })
        data['todos'] = todos

    return data


def store():
    try:
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']

        users = Users(name=name, email=email)
        users.setPassword(password)
        db.session.add(users)
        db.session.commit()
        return response.ok('', "User added successfully")
    except Exception as error:
        print(f'Failed to connect: {error}')

def update(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], "User not found")

        # Update user fields if present in the request JSON
        if 'name' in request.json:
            user.name = request.json['name']
        if 'email' in request.json:
            user.email = request.json['email']
        if 'password' in request.json:
            user.setPassword(request.json['password'])

        Users.updated_at = datetime.utcnow()
        db.session.commit()

        return response.ok([], "Success update data")
    except Exception as error:
        print(f'Failed to connect: {error}')

def delete(id):
    try:
        user = Users.query.filter_by(id=id).first()
        if not user:
            return response.badRequest([], "User not found")

        db.session.delete(user)
        db.session.commit()

        return response.ok([], "Success delete user")
    except Exception as error:
        print(f'Failed to connect: {error}')
        return response.internalServerError([], "Failed to delete user")