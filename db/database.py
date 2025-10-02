from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_DB_URI"))
db = client["task_manager"]
task_collection = db["tasks"]
user_collection = db["users"]