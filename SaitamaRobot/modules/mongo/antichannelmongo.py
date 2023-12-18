from SaitamaRobot import CHAT_DB
from pymongo import MongoClient

# Initialize MongoDB client and collection
antichanneldb = MongoClient(CHAT_DB)["KUKI"]["antichannel"]

def antichannel_status(chat_id):
    return antichanneldb.find_one({"chat_id": chat_id}) is not None

def enable_antichannel(chat_id):
    if not antichannel_status(chat_id):
        antichanneldb.insert_one({"chat_id": chat_id})

def disable_antichannel(chat_id):
    if antichannel_status(chat_id):
        antichanneldb.delete_one({"chat_id": chat_id})
