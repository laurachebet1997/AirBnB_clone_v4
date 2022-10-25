#!/usr/bin/python3
"""
Script for the cities API RESTful API
"""
from api.v1.views import app_views, State, City
from flask import jsonify, abort, request
from models import storage


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET'])
def get_cities_state(state_id):
    """ Method for the "/states/<state_id>/cities" path GET
    Returns cities by state
    ---
    tags:
      -   City
    parameters:
      - name: state_id
        in: path
        type: string
        required: true
        description: The ID of State, try 2b9a4627-8a9e-4f32-a752-9a84fa7f4efd
    responses:
      200:
        description: An array of City objects
        examples:
          [
            {
              "__class__": "City",
              "created_at": "2017-03-25T02:17:06",
              "id": "1da255c0-f023-4779-8134-2b1b40f87683",
              "name": "New Orleans",
              "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
              "updated_at": "2017-03-25T02:17:06"
            },
            {
              "__class__": "City",
              "created_at": "2017-03-25T02:17:06",
              "id": "45903748-fa39-4cd0-8a0b-c62bfe471702",
              "name": "Lafayette",
              "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
              "updated_at": "2017-03-25T02:17:06"
            },
            {
              "__class__": "City",
              "created_at": "2017-03-25T02:17:06",
              "id": "e4e40a6e-59ff-4b4f-ab72-d6d100201588",
              "name": "Baton rouge",
              "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
              "updated_at": "2017-03-25T02:17:06"
            }
          ]
      404:
        description: When state_id not found
    """
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities), 200
    return abort(404)


    @app_views.route('/cities/<city_id>', strict_slashes=False, methods=['GET'])
def get_city(city_id):
    """ Method for the "/cities/<city_id>" path GET
    Returns City by id
    ---
    tags:
      -   City
    parameters:
      - name: city_id
        in: path
        type: string
        required: true
        description: The ID of State, try 1da255c0-f023-4779-8134-2b1b40f87683
    responses:
      200:
        description: A State object
        examples:
          {
            "__class__": "City",
            "created_at": "2017-03-25T02:17:06",
            "id": "1da255c0-f023-4779-8134-2b1b40f87683",
            "name": "New Orleans",
            "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
            "updated_at": "2017-03-25T02:17:06"
          }
      404:
        description: When city_id not found
    """
    city = storage.get(City, city_id)
    if city:
        city = city.to_dict()
        return jsonify(city), 200
    return abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['DELETE'])
def delete_city(city_id):
    """ Method for the "/cities/<city_id>" path DELETE
    Removes City by id
    ---
    tags:
      -   City
    parameters:
      - name: city_id
        in: path
        type: string
        required: true
        description: The ID of State, create one and try its ID
    responses:
      200:
        description: Object deleted
        examples:
            {}
      404:
        description: When city_id not found
    """
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    return abort(404)


    @app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['POST'])
def create_city(state_id):
    """ Method for the "/states/<state_id>/cities" path POST
    Creates a new City
    ---
    tags:
      -   City
    parameters:
      - in: body
        name: body
        required: true
        content:
          application/json:
        schema:
          properties:
            name:
              type: string
              description: Name for the city, try Alexandria
      - in: path
        name: state_id
        type: string
        required: true
        description: The ID of State, try 2b9a4627-8a9e-4f32-a752-9a84fa7f4efd
    responses:
      201:
        description: A State object was created
        examples:
          {
            "__class__": "City",
            "created_at": "2017-04-16T03:14:05.655490",
            "id": "b75ae104-a8a3-475e-bf74-ab0a066ca2af",
            "name": "Alexandria",
            "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
            "updated_at": "2017-04-16T03:14:05.655748"
          }
      400:
        description: When error in JSON or in data
        examples:
          {
            "error": "Not a JSON"
          }
        examples:
          {
            "error": "Missing name"
          }
      404:
        description: When state_id not found
    """
    body = request.get_json(silent=True)
    state = storage.get(State, state_id)
    if not bool(state):
        return abort(404)


     body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'name' in body:
        new_city = City(**body)
        new_city.state_id = state.id
        storage.new(new_city)
        storage.save()
        return jsonify(new_city.to_dict()), 201
    else:
        return jsonify({'error': 'Missing name'}), 400


@app_views.route('/cities/<city_id>', strict_slashes=False, methods=['PUT'])
def update_city(city_id):
    """ Method for the "/cities/<city_id>" path PUT
    Updates a City
    ---
    tags:
      -   City
    parameters:
      - in: body
        name: body
        required: true
        content:
          application/json:
        schema:
          properties:
            name:
              type: string
              description: Name for the city, try Bossier City
      - in: path
        name: city_id
        type: string
        required: true
        description: The ID of State, try b75ae104-a8a3-475e-bf74-ab0a066ca2af
    responses:
      200:
        description: A State object was modified
        examples:
          {
            "__class__": "City",
            "created_at": "2017-04-16T03:14:06",
            "id": "b75ae104-a8a3-475e-bf74-ab0a066ca2af",
            "name": "Bossier City",
            "state_id": "2b9a4627-8a9e-4f32-a752-9a84fa7f4efd",
            "updated_at": "2017-04-16T03:15:12.895894"
          }
      400:
        description: When error in JSON
        examples:
          {
            "error": "Not a JSON"
          }
      404:
        description: When city_id not found
    """
    city = storage.get(City, city_id)
    if city:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            print(city.__class__.name)
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(city, key, body[key])
        city.save()
        return jsonify(city.to_dict()), 200
    return abort(404)
