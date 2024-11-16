from werkzeug.security import check_password_hash, generate_password_hash
from bson import ObjectId

class User:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, username, password):
        user = {
            "username": username,
            "password": generate_password_hash(password)
        }
        return self.collection.insert_one(user)
    
    def find_by_username(self, username):
        return self.collection.find_one({"username": username})
    
    def check_password(self, user, password):
        return check_password_hash(user["password"], password)
    
    def get_username_by_id(self, user_id):
        return self.collection.find_one({"_id": ObjectId(user_id)})