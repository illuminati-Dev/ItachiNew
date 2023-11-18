import threading
from sqlalchemy import Column, String, exists
from sqlalchemy.orm import sessionmaker
from SaitamaRobot.modules.sql import BASE, SESSION

class NSFWChats(BASE):
    __tablename__ = "henati_chats"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id

NSFWChats.__table__.create(checkfirst=True)
INSERTION_LOCK = threading.RLock()
Session = sessionmaker(bind=SESSION)


def is_hentai(chat_id):
    with Session() as session:
        return session.query(exists().where(NSFWChats.chat_id == str(chat_id))).scalar()

def set_hentai(chat_id):
    with INSERTION_LOCK, Session() as session:
        nsfwchat = session.query(NSFWChats).get(str(chat_id))
        if not nsfwchat:
            nsfwchat = NSFWChats(str(chat_id))
            session.add(nsfwchat)
            session.commit()

def rem_hentai(chat_id):
    with INSERTION_LOCK, Session() as session:
        nsfwchat = session.query(NSFWChats).get(str(chat_id))
        if nsfwchat:
            session.delete(nsfwchat)
            session.commit()

def get_all_hentai_chats():
    with Session() as session:
        return [chat.chat_id for chat in session.query(NSFWChats.chat_id).all()]
