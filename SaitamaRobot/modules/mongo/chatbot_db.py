from pymongo import MongoClient
from SaitamaRobot import CHAT_DB

cha_db = MongoClient(CHAT_DB)["KUKIAI"]["CHATS"]


class Chat:
    def __init__(self, chat_id):
        self.chat_id = chat_id

    def is_ai_chat(chat_id):
        if cha_db.find_one({"chat_id": chat_id}):
            return True
        else:
            return False

    def add_ai(chat_id):
        if not Chat.is_ai_chat(chat_id):
            cha_db.insert_one({"chat_id": chat_id})
        else:
            return

    def rm_ai(chat_id):
        if Chat.is_ai_chat(chat_id):
            cha_db.delete_one({"chat_id": chat_id})
        else:
            return

    def get_ai_chats():
        return cha_db.find()
