#!/usr/bin/python3
"""
Route
"""

from api.v1.views import app_views, User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET'])
def all_users():
    """ Method for the "/users" path GET
    Returns all users
    ---
    tags:
      - User
    responses:
      200:
        description: A list of all User objects
        examples:
          [
            {
              "__class__":"User",
              "created_at":"2017-03-25T02:17:06.000000",
              "email":"noemail20@gmail.com",
              "first_name":"Leon",
              "id":"fa44780d-ac48-41ab-9dd0-ac54a15755cf",
              "last_name":"Sarro",
              "password":"pwd20",
              "updated_at":"2017-03-25T02:17:06.000000"
            },
            {
              "__class__":"User",
              "created_at":"2017-03-25T02:17:06.000000",
              "email":"noemail23@gmail.com",
              "first_name":"Cecilia",
              "id":"150e591e-486b-48ee-be42-4aecba665020",
              "last_name":"Boes",
              "password":"pwd23",
              "updated_at":"2017-03-25T02:17:06.000000"
            }
          ]
    """
    users = storage.all(User)
    users = [user.to_dict() for user in users.values()]
    return jsonify(users), 200


@app_views.route('/users/<id>', strict_slashes=False, methods=['GET'])
def get_user(id):
    """ Method for the "/users/<id>" path GET
    Returns User by id
    ---
    tags:
      - User
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of User, try fa44780d-ac48-41ab-9dd0-ac54a15755cf
    responses:
      200:
        description: A User object
        examples:
          {
            "__class__":"User",
            "created_at":"2017-03-25T02:17:06.000000",
            "email":"noemail20@gmail.com",
            "first_name":"Leon",
            "id":"fa44780d-ac48-41ab-9dd0-ac54a15755cf",
            "last_name":"Sarro",
            "password":"pwd20",
            "updated_at":"2017-03-25T02:17:06.000000"
          }
      404:
        description: When id not found
    """
    user = storage.get(User, id)
    if user:
        user = user.to_dict()
        return jsonify(user), 200
    return abort(404)


@app_views.route('/users/<id>', strict_slashes=False, methods=['DELETE'])
def delete_user(id):
    """Removes user by id"""
    user = storage.get(User, id)
    if user:
        storage.delete(user)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/users', strict_slashes=False, methods=['POST'])
def create_user():
    """Creates a new user"""
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'email' not in body:
        return jsonify({'error': 'Missing email'}), 400
    if 'password' not in body:
        return jsonify({'error': 'Missing password'}), 400
    new_user = User(**body)
    storage.new(new_user)
    storage.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<id>', strict_slashes=False, methods=['PUT'])
def update_user(id):
    """Updates a user"""
    user = storage.get(User, id)
    if user:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(user, key, body[key])
        user.save()
        return jsonify(user.to_dict()), 200
    return abort(404)
