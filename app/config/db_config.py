from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv('DATABASE_URL')
# Initialize MongoDB connection

client = MongoClient(uri)

db = client[f"{os.getenv('MONGO_INITDB_DATABASE')}"]

user_collection = db['users']
candidate_collection = db['candidates']

candidate_collection.create_index([("first_name", "text"),
    ("last_name", "text"),
    ("email", "text"),
    ("career_level", "text"),
    ("job_major", "text"),
    ("degree_type", "text"),
    ("skills", "text"),
    ("nationality", "text"),
    ("city", "text")
])

try:
    client.admin.command('ping')
    print("Connected to Mongo")
except Exception as e:
    print(e)