from pymongo import MongoClient

# Initialize MongoDB connection
client = MongoClient('mongodb://localhost:27017')
db = client['recruitment-apis']

# Access collections
user_collection = db['users']
candidate_collection = db['candidates']