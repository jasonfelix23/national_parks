from flask import Blueprint, request, jsonify
from models.park_visit import ParkVisit
from models.user import User
from app import db
from bson import ObjectId
import datetime
from utils.auth import token_required
from utils.json_response import json_response

park_visit_bp = Blueprint('park_visit', __name__)
park_visit_model = ParkVisit(db)
user_model = User(db)


@park_visit_bp.route("/", methods=['POST'])
@token_required
def add_visit(current_user):
    data = request.json
    print(data)
    park_id = data['park_id']
    visit_date = datetime.datetime.strptime(data['visit_date'], '%Y-%m-%d')
    status = data['status']

    result = park_visit_model.add_visit(current_user, park_id, visit_date, status)
    return json_response({"message": "Visit added successfully", "id": str(result.inserted_id)}, 201)

@park_visit_bp.route("/user", methods=['GET'])
@token_required
def get_user_visits(current_user):
    user =  user_model.get_username_by_id(current_user)
    print(user['username'])
    visits = park_visit_model.get_user_visits(current_user)
    visit_data = [{'_id': str(visit['_id']), **visit} for visit in visits]
    visit_data = [{k: str(v) if isinstance(v, ObjectId) else v for k, v in visit.items()} for visit in visit_data]
    return json_response( {'username': user['username'], 'visits': visit_data}, 200)

@park_visit_bp.route("/<visit_id>", methods=["PUT"])
@token_required
def update_visit(current_user, visit_id):
    data = request.json
    print("UPDATING-----------")
    print(data)
    data['visit_date'] = datetime.datetime.strptime(data['visit_date'], '%Y-%m-%d')
    result = park_visit_model.update_vists(current_user, visit_id, data)

    if result.modified_count:
        return json_response({"message": "Visit updated successfully"}, 200)
    return json_response({"message": "Visit not found or no changes made"}, 404)

@park_visit_bp.route("/<visit_id>", methods=['DELETE'])
@token_required
def delete_visit(current_user, visit_id):
    result = park_visit_model.delete_visit(current_user, visit_id)
    if result.deleted_count:
        return json_response({"message": "Visit deleted successfully"}, 200)
    return json_response({"message": "visit not found"}, 404)