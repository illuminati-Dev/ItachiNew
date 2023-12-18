import threading

from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    UnicodeText,
    UniqueConstraint,
    func,
)

from SaitamaRobot import dispatcher
from SaitamaRobot.modules.sql import BASE, SESSION
from sqlalchemy.sql.sqltypes import BigInteger

class Users(BASE):
    __tablename__ = "users"
    user_id = Column(BigInteger, primary_key=True)
    username = Column(UnicodeText)

    def __init__(self, user_id, username=None):
        self.user_id = user_id
        self.username = username

    def __repr__(self):
        return "<User {} ({})>".format(self.username, self.user_id)


class Chats(BASE):
    __tablename__ = "chats"
    chat_id = Column(String(14), primary_key=True)
    chat_name = Column(UnicodeText, nullable=False)

    def __init__(self, chat_id, chat_name):
        self.chat_id = str(chat_id)
        self.chat_name = chat_name

    def __repr__(self):
        return "<Chat {} ({})>".format(self.chat_name, self.chat_id)


class ChatMembers(BASE):
    __tablename__ = "chat_members"
    priv_chat_id = Column(BigInteger, primary_key=True)
    chat_id = Column(
        String(14),
        ForeignKey("chats.chat_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    user_id = Column(
        BigInteger,
        ForeignKey("users.user_id", onupdate="CASCADE", ondelete="CASCADE"),
        nullable=False,
    )
    __table_args__ = (UniqueConstraint("chat_id", "user_id", name="_chat_members_uc"),)

    def __init__(self, chat_id, user_id):
        self.chat_id = chat_id
        self.user_id = user_id

    def __repr__(self):
        return "<Chat user {} ({}) in chat {} ({})>".format(
            self.user.username,
            self.user.user_id,
            self.chat.chat_name,
            self.chat.chat_id,
        )


Users.__table__.create(checkfirst=True)
Chats.__table__.create(checkfirst=True)
ChatMembers.__table__.create(checkfirst=True)

INSERTION_LOCK = threading.RLock()


def ensure_bot_in_db():
    with INSERTION_LOCK:
        bot = Users(user_id=dispatcher.bot.id, username=dispatcher.bot.username)
        SESSION.merge(bot)
        SESSION.commit()


def update_user(user_id, username, chat_id=None, chat_name=None):
    with INSERTION_LOCK:
        user = SESSION.query(Users).get(user_id)
        if not user:
            user = Users(user_id=user_id, username=username)
            SESSION.add(user)
            SESSION.flush()
        else:
            user.username = username

        if not chat_id or not chat_name:
            SESSION.commit()
            return

        chat = SESSION.query(Chats).get(str(chat_id))
        if not chat:
            chat = Chats(chat_id=str(chat_id), chat_name=chat_name)
            SESSION.add(chat)
            SESSION.flush()

        else:
            chat.chat_name = chat_name

        member = (
            SESSION.query(ChatMembers)
            .filter(ChatMembers.chat_id == chat.chat_id, ChatMembers.user_id == user.user_id)
            .first()
        )
        if not member:
            chat_member = ChatMembers(chat_id=chat.chat_id, user_id=user.user_id)
            SESSION.add(chat_member)

        SESSION.commit()


def get_userid_by_name(username):
    try:
        return (
            SESSION.query(Users)
            .filter(func.lower(Users.username) == username.lower())
            .all()
        )
    finally:
        SESSION.close()


def get_name_by_userid(user_id):
    try:
        return SESSION.query(Users).get(user_id).username
    finally:
        SESSION.close()


def get_chat_members(chat_id):
    try:
        return SESSION.query(ChatMembers).filter(ChatMembers.chat_id == str(chat_id)).all()
    finally:
        SESSION.close()


def get_all_chats():
    try:
        return SESSION.query(Chats).all()
    finally:
        SESSION.close()


def get_all_users():
    try:
        return SESSION.query(Users).all()
    finally:
        SESSION.close()


def get_user_num_chats(user_id):
    try:
        return (
            SESSION.query(ChatMembers).filter(ChatMembers.user_id == int(user_id)).count()
        )
    finally:
        SESSION.close()


def get_user_com_chats(user_id):
    try:
        chat_members = (
            SESSION.query(ChatMembers).filter(ChatMembers.user_id == int(user_id)).all()
        )
        return [i.chat_id for i in chat_members]
    finally:
        SESSION.close()


def num_chats():
    try:
        return SESSION.query(Chats).count()
    finally:
        SESSION.close()


def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()


def migrate_chat(old_chat_id, new_chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Chats).get(str(old_chat_id))
        if chat:
            chat.chat_id = str(new_chat_id)
        SESSION.commit()

        chat_members = (
            SESSION.query(ChatMembers)
            .filter(ChatMembers.chat_id == str(old_chat_id))
            .all()
        )
        for member in chat_members:
            member.chat_id = str(new_chat_id)
        SESSION.commit()


ensure_bot_in_db()


def del_user(user_id):
    with INSERTION_LOCK:
        curr = SESSION.query(Users).get(user_id)
        if curr:
            SESSION.delete(curr)
            SESSION.commit()
            return True

        ChatMembers.query.filter(ChatMembers.user_id == user_id).delete()
        SESSION.commit()
        SESSION.close()
    return False


def rem_chat(chat_id):
    with INSERTION_LOCK:
        chat = SESSION.query(Chats).get(str(chat_id))
        if chat:
            SESSION.delete(chat)
            SESSION.commit()
        else:
            SESSION.close()
