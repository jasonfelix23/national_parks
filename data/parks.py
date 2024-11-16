import csv
import pymongo
from datetime import datetime
import re

# MongoDB connection details
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "national_parks_db"
COLLECTION_NAME = "parks"

# Connect to MongoDB
client = pymongo.MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

# CSV file path
CSV_FILE_PATH = "USNationalParks.csv"

# Function to clean latitude and longitude
def clean_coordinates(coord):
    return float(re.search(r'-?\d+\.\d+', coord).group())

# Function to parse date
def parse_date(date_string):
    return datetime.strptime(date_string, "%B %d, %Y")

# Function to clean numeric values
def clean_numeric(value):
    return float(re.sub(r'[^\d.]', '', value))

# Read CSV and insert data into MongoDB
with open(CSV_FILE_PATH, 'r', encoding='utf-8-sig') as csvfile:
    csv_reader = csv.DictReader(csvfile)
    
    for row in csv_reader:
        print(row)
        park_data = {
            "park_name": row["park"].strip(),
            "location": {
                "type": "Point",
                "coordinates": [
                    clean_coordinates(row["Longitude"]),
                    clean_coordinates(row["Latitude"])
                ]
            },
            "primary_location": row["Primary_location"].strip(),
            "date_established": parse_date(row["date_established"]),
            "area_in_acres": clean_numeric(row["area_in_acres"]),
            "area_in_kms": clean_numeric(row["area_in_kms"]),
            "visits": int(clean_numeric(row["visits"])),
            "description": row["Description"].strip()
        }
        
        # Insert the document into MongoDB
        collection.insert_one(park_data)

print("Data import completed successfully!")

# Create a geospatial index on the location field
# collection.create_index([("location", "2dsphere")])

# Close the MongoDB connection
client.close()