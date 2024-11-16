from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app, 
     supports_credentials=True, 
     origins=["*"], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"])

mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
db_name = os.getenv("DB_NAME", "national_parks_db")
mongo_client = MongoClient(mongo_uri)
db = mongo_client[db_name]

from controllers.auth_controller import auth_bp
from controllers.park_visit_controller import park_visit_bp
from controllers.national_park_controller import national_park_bp

app.register_blueprint(auth_bp, url_prefix="/api/auth")
app.register_blueprint(park_visit_bp, url_prefix="/api/visits")
app.register_blueprint(national_park_bp, url_prefix="/api/parks")

@app.route("/")
def hello_world():
    return "Hello, World!"

if __name__== "__main__":
    app.run(debug=True)

