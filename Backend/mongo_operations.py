from pymongo.mongo_client import MongoClient
from pymongo import errors
from pymongo.server_api import ServerApi
import os
from dotenv import load_dotenv
import certifi
ca = certifi.where()
load_dotenv()

client = MongoClient(os.getenv('MONGO_URI'), server_api=ServerApi('1'), tlsCAFile=ca)

shs_app_db = client["shs_app"]
users_col = shs_app_db["users"]

def insert_user(user_data):
    try:
        users_col.insert_one(user_data)
    except errors.DuplicateKeyError as e:
        raise e

def get_user_by_email_hash(email_hash):
    return users_col.find_one({"email_hash": email_hash})

# def get_user_by_totp_hash(totp_hash):
#     return users_col.find_one({"totp_hash": totp_hash})

def get_patients():
    return users_col.find({"role": {"$not": {"$regex": "Doctor"}}})
