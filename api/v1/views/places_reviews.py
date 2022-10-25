#!/usr/bin/python3
"""
Script for the cities API RESTful API
"""
from api.v1.views import app_views, Place, Review, User
from flask import jsonify, abort, request
from models import storage


@app_views.route('/places/<place_id>/reviews', strict_slashes=False,
                 methods=['GET'])
def get_reviews_places(place_id):
    """ Method for the "/places/<place_id>/reviews" path GET
    Returns reviews by place
    ---
    tags:
      - Review
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: place_id
        in: path
        type: string
        required: true
        description: The ID of Place, try 279b355e-ff9a-4b85-8114-6db7ad2a4cd2
    responses:
      200:
        description: An array of Review objects
        examples:
          [
            {
              "__class__":"Review",
              "created_at":"2017-03-25T02:17:07.000000",
              "id":"3f54d114-582d-4dab-8559-f0682dbf1fa6",
              "place_id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "text":"Really nice place and really nice people. Secluded. Everything was clean. Very convenient. You will love it.",
              "updated_at":"2017-03-25T02:17:07.000000",
              "user_id":"887dcd8d-d5ee-48de-9626-73ff4ea732fa"
            },
            {
              "__class__":"Review",
              "created_at":"2017-03-25T02:17:07.000000",
              "id":"78388983-b5a5-47af-8ebd-e7f005540831",
              "place_id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
              "text":"Perfect for our one night stay in New Orleans. Clean & comfortable.",
              "updated_at":"2017-03-25T02:17:07.000000",
              "user_id":"7231eaa1-400f-4cb5-a867-f5eba8adbb81"
            }
          ]
      404:
        description: When place_id not found
    """
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews), 200
    return abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['GET'])
def get_review(review_id):
    """ Method for the "/reviews/<review_id>" path GET
    Returns Review by id
    ---
    tags:
      - Review
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - name: review_id
        in: path
        type: string
        required: true
        description: The ID of State, try 3f54d114-582d-4dab-8559-f0682dbf1fa6
    responses:
      200:
        description: A State object
        examples:
          {
            "__class__":"Review",
            "created_at":"2017-03-25T02:17:07.000000",
            "id":"3f54d114-582d-4dab-8559-f0682dbf1fa6",
            "place_id":"279b355e-ff9a-4b85-8114-6db7ad2a4cd2",
            "text":"Really nice place and really nice people. Secluded. Everything was clean. Very convenient. You will love it.",
            "updated_at":"2017-03-25T02:17:07.000000",
            "user_id":"887dcd8d-d5ee-48de-9626-73ff4ea732fa"
          }
      404:
        description: When review_id not found
    """
    review = storage.get(Review, review_id)
    if review:
        review = review.to_dict()
        return jsonify(review), 200
    return abort(404)


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['DELETE'])
def delete_review(review_id):
    """Removes place by id"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    return abort(404)


@app_views.route('/places/<places_id>/reviews', strict_slashes=False,
                 methods=['POST'])
def create_review(places_id):
    """Creates a new place"""
    place = storage.get(Place, places_id)
    if not bool(place):
        return abort(404)

    body = request.get_json(silent=True)
    if body is None:
        return jsonify({'error': 'Not a JSON'}), 400

    if 'user_id' not in body:
        return jsonify({'error': 'Missing user_id'}), 400
    user = storage.get(User, body.get('user_id'))
    if not bool(user):
        return abort(404)

    if 'text' in body:
        new_review = Review(**body)
        setattr(new_review, 'place_id', place.id)
        storage.new(new_review)
        storage.save()
        return jsonify(new_review.to_dict()), 201
    else:
        return jsonify({'error': 'Missing text'}), 400


@app_views.route('/reviews/<review_id>', strict_slashes=False, methods=['PUT'])
def update_review(review_id):
    """Updates a place"""
    review = storage.get(Review, review_id)
    if review:
        body = request.get_json(silent=True)
        if body is None:
            return jsonify({'error': 'Not a JSON'}), 400
        for key in body:
            if key != 'id' and key != 'user_id' and key != 'place_id'\
                    and key != 'created_at' and key != 'updated_at':
                setattr(review, key, body.get(key))
        review.save()
        return jsonify(review.to_dict()), 200
    return abort(404)
