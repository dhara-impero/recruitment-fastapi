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

try:
    client.admin.command('ping')
    print("Connected to Mongo")
except Exception as e:
    print(e)