from flask import Blueprint, jsonify, request
from models.national_park import NationalPark
from utils.json_response import json_response
from app import db

national_park_bp = Blueprint('national_park', __name__)
national_park_model = NationalPark(db)

@national_park_bp.route("/", methods=['GET'])
def get_all_parks():
    parks = national_park_model.get_all_parks()
    return json_response([{**park, "_id": str(park['_id'])} for park in parks], 200)

@national_park_bp.route("/<park_id>", methods=["GET"])
def get_park(park_id):
    park = national_park_model.get_park_by_id(park_id)
    if park:
        park['_id'] = str(park['_id'])
        return json_response(park, 200)
    return json_response({"message": "Park not found"}, 404)

@national_park_bp.route('/search', methods=['GET'])
def search_parks():
    query = request.args.get('q', '')
    parks = national_park_model.search_parks(query)
    return json_response([{**park, '_id': str(park['_id'])} for park in parks], 200)