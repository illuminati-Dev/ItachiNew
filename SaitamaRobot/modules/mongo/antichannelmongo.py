from SaitamaRobot import CHAT_DB
from pymongo import MongoClient

antichanneldb = MongoClient(CHAT_DB)["KUKI"]["antichannel"]

def antichannel_status(chat_id):
    is_achannel = antichanneldb.find_one({"chat_id": chat_id})
    if not is_achannel:
        return False
    else:
        return True

def enable_antichannel(chat_id):
    is_achannel = antichannel_status(chat_id)
    if is_achannel:
        return
    else:
        return antichanneldb.insert_one({"chat_id": chat_id})

def disable_antichannel(chat_id):
    is_achannel = antichannel_status(chat_id)
    if not is_achannel:
        return
    else:
        return antichanneldb.delete_one({"chat_id": chat_id})
