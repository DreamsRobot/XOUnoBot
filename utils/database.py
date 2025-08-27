from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["xo_uno_bot"]

def get_collection(name):
    return db[name]
