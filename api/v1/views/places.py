#!/usr/bin/python3
"""
Route Places
"""

from api.v1.views import app_views, Place, City, User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['GET'])
def get_city_place(id):
    """ Method for the "/cities/<id>/places" path GET
    Returns all Place objects in a City
    ---
    tags:
      - Place
    responses:
      200:
        description: A list of all Place objects
        examples:
          [
            {
              "__class__":"Place",
              "city_id":"1da255c0-f023-4779-8134-2b1b40f87683",
              "created_at":"2017-03-25T02:17:06.000000",
              "description":"The guest house is located uptown two blocks ...",
              "id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "latitude":29.9493,
              "longitude":-90.1171,
              "max_guest":2,
              "name":"Guest House by Tulane",
              "number_bathrooms":1,
              "number_rooms":0,
              "price_by_night":60,
              "updated_at":"2017-03-25T02:17:06.000000",
              "user_id":"8394fd35-8a8a-479f-a398-48f53b4a6554"
            },
            {
              "__class__":"Place",
              "city_id":"1da255c0-f023-4779-8134-2b1b40f87683",
              "created_at":"2017-03-25T02:17:06.000000",
              "description":"Semi-private room in a cute and cozy shotgun ...",
              "id":"ffcc9c22-759e-4418-b788-81eda89c2865",
              "latitude":29.9666,
              "longitude":-90.0519,
              "max_guest":1,
              "name":"Affordable room in the Marigny",
              "number_bathrooms":1,
              "number_rooms":1,
              "price_by_night":40,
              "updated_at":"2017-03-25T02:17:06.000000",
              "user_id":"7771bbe9-92ab-46d1-a636-864526361d7d"
            }
          ]
      404:
        description: When data not found
    """
     city = storage.get(City, id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places), 200
    return abort(404)


@app_views.route('/places/<id>', strict_slashes=False, methods=['GET'])
def get_place(id):
    """ Method for the "/places/<id>" path GET
    Returns Place by id
    ---
    tags:
      - Place
    parameters:
      - name: id
        in: path
        type: string
        required: true
        description: The ID of Place, try 279b355e-ff9a-4b85-8114-6db7ad2a4cd2
    responses:
      200:
        description: A Place object
        examples:
          {
            "__class__":"Place",
            "city_id":"1da255c0-f023-4779-8134-2b1b40f87683",
            "created_at":"2017-03-25T02:17:06.000000",
            "description":"The guest house is located uptown two blocks ...",
            "id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
            "latitude":29.9493,
            "longitude":-90.1171,
            "max_guest":2,
            "name":"Guest House by Tulane",
            "number_bathrooms":1,
            "number_rooms":0,
            "price_by_night":60,
            "updated_at":"2017-03-25T02:17:06.000000",
            "user_id":"8394fd35-8a8a-479f-a398-48f53b4a6554"
          }
      404:
        description: When id not found
    """
    place = storage.get(Place, id)
    if place:
        place = place.to_dict()
        return jsonify(place), 200
    return abort(404)


@app_views.route('/places/<id>', strict_slashes=False, methods=['DELETE'])
def delete_place(id):
    """Removes place by id"""
    place = storage.get(Place, id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/cities/<id>/places', strict_slashes=False, methods=['POST'])
def create_place(id):
    """Creates a new place"""
    city_exist = storage.get(City, id)
    if city_exist is None:
        return abort(404)
    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400
    if 'user_id' not in body:
        return jsonify({'error': 'Missing user_id'}), 400
    user_exist = storage.get(User, body['user_id'])
    if user_exist is None:
        return abort(404)
    if 'name' not in body:
        return jsonify({'error': 'Missing name'}), 400
    new_place = Place(**body)
    setattr(new_place, 'city_id', id)
    storage.new(new_place)
    storage.save()
    return jsonify(new_place.to_dict()), 201


@app_views.route('/places/<id>', strict_slashes=False, methods=['PUT'])
def update_place(id):
    """Updates a place"""
    place = storage.get(Place, id)
    if place:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        if 'user_id' in body:
            user_exist = storage.get(User, body['user_id'])
            if user_exist is None:
                return abort(404)
        for key in body:
            if key != 'id' and key != 'created_at' and key != 'updated_at'\
                    and key != 'user_id' and key != 'city_id':
                setattr(place, key, body[key])
        place.save()
        return jsonify(place.to_dict()), 200
    return abort(404)
