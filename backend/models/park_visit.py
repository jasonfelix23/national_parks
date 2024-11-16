from bson import ObjectId

class ParkVisit:
    def __init__(self, db):
        self.collection = db.park_visits

    def add_visit(self, user_id, park_id, visit_date, status):
        visit={
            "user_id": ObjectId(user_id),
            "park_id": ObjectId(park_id),
            "visit_date": visit_date,
            "status": status
        }
        return self.collection.insert_one(visit)
    
    def get_user_visits(self, user_id):
        return list(self.collection.find({"user_id": ObjectId(user_id)}))

    def update_vists(self, user_id, visit_id, update_data):
        print(visit_id+ "trying to update")
        return self.collection.update_one({"_id": ObjectId(visit_id), "user_id": ObjectId(user_id)}, {"$set": update_data})
    
    def delete_visit(self, user_id, visit_id):
        return self.collection.delete_one({"_id": ObjectId(visit_id), "user_id": ObjectId(user_id)})