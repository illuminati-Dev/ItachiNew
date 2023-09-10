import threading
from sqlalchemy import Column, String
from SaitamaRobot.modules.sql import BASE, SESSION
#   |----------------------------------|
#   |  Test Module by @EverythingSuckz |
#   |        Kang with Credits         |
#   |----------------------------------|
class NSFWChats(BASE):
    __tablename__ = "henati_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

NSFWChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()


def is_hentai(chat_id):
    try:
        chat = SESSION.query(NSFWChats).get(str(chat_id))
        return bool(chat)
    finally:
        SESSION.close()

def set_hentai(chat_id):
    with INSERTION_LOCK:
        nsfwchat = SESSION.query(NSFWChats).get(str(chat_id))
        if not nsfwchat:
            nsfwchat = NSFWChats(str(chat_id))
        SESSION.add(nsfwchat)
        SESSION.commit()

def rem_hentai(chat_id):
    with INSERTION_LOCK:
        nsfwchat = SESSION.query(NSFWChats).get(str(chat_id))
        if nsfwchat:
            SESSION.delete(nsfwchat)
        SESSION.commit()


def get_all_hentai_chats():
    try:
        return SESSION.query(NSFWChats.chat_id).all()
    finally:
        SESSION.close()
