from bson import ObjectId

class NationalPark:
    def __init__(self, db):
        self.collection = db.parks

    def get_all_parks(self):
        return list(self.collection.find())
    
    def get_park_by_id(self, park_id):
        return self.collection.find_one({"_id": ObjectId(park_id)})
    
    def search_parks(self, query):
        return list(self.collection.find({"$text": {"$search": query}}))