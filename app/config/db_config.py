from pymongo.mongo_client import MongoClient

# Initialize MongoDB connection
uri = "mongodb+srv://dharaimpero:adDYA129W1w98B3i@recruitment.jiq3r.mongodb.net/"

client = MongoClient(uri)

db = client['recruitment']

user_collection = db['users']
candidate_collection = db['candidates']

try:
    client.admin.command('ping')
    print("Connected to Mongo")
except Exception as e:
    print(e)