from typing import Optional
import time
import random
from datetime import datetime
import humanize

from telegram import Message, User, Update
from telegram import MessageEntity, ParseMode
from telegram.error import BadRequest
from telegram.ext import Filters, MessageHandler, run_async

from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler, DisableAbleMessageHandler
from SaitamaRobot.modules.redis.afk_redis import start_afk, end_afk, is_user_afk, afk_reason
from SaitamaRobot import REDIS
from SaitamaRobot.modules.users import get_user_id

from SaitamaRobot.modules.helper_funcs.alternate import send_message
from SaitamaRobot.modules.helper_funcs.readable_time import get_readable_time

AFK_GROUP = 7
AFK_REPLY_GROUP = 8

def afk(update, context):
    args = update.effective_message.text.split(None, 1)
    user = update.effective_user
    if not user:  # ignore channels
        return

    if user.id == 777000:
        return
    start_afk_time = time.time()
    reason = args[1] if len(args) >= 2 else "none"
    start_afk(user.id, reason)
    REDIS.set(f'afk_time_{user.id}', start_afk_time)
    fname = user.first_name
    try:
        update.effective_message.reply_text(f"{fname} is now Away!")
    except BadRequest:
        pass

def no_longer_afk(update, context):
    user = update.effective_user
    message = update.effective_message
    if not user:  # ignore channels
        return

    if not is_user_afk(user.id):  #Check if user is afk or not
        return
    end_afk_time = get_readable_time((time.time() - float(REDIS.get(f'afk_time_{user.id}'))))
    REDIS.delete(f'afk_time_{user.id}')
    if res := end_afk(user.id):
        if message.new_chat_members:  # dont say msg
            return
        firstname = user.first_name
        try:
            options = [
                "{} Is wasting his time in the chat!",
                "The Dead {} Came Back From His Grave!\nTime you were AFK for: {}",
                "We thought we lost you {}\nTime you were AFK for: {}",
                "Welcome Back {} now pay $100 to Get freedom or get banned!\nTime you were AFK for: {}",
                "{} Good job waking up now get ready for your classes!\nTime you were AFK for: {}",
                "Hey {}! Why weren't you online for such a long time?\nTime you were AFK for: {}",
                "{} why did you came back?\nTime you were AFK for: {}",
                "{} Is now back online!\nTime you were AFK for: {}",
                "OwO, Welcome back {}\nTime you were AFK for: {}",
                "Welcome to hell again {}\nTime you were AFK for: {}",
                "Mission failed successfully {}\nTime you were AFK for: {}",
            ]
            chosen_option = random.choice(options)
            update.effective_message.reply_text(
                chosen_option.format(firstname, end_afk_time),
            )
        except Exception:
            return
            



def reply_afk(update, context):
    message = update.effective_message
    userc = update.effective_user
    userc_id = userc.id
    if message.entities and message.parse_entities(
        [MessageEntity.TEXT_MENTION, MessageEntity.MENTION]):
        entities = message.parse_entities(
            [MessageEntity.TEXT_MENTION, MessageEntity.MENTION])

        chk_users = []
        for ent in entities:
            if ent.type == MessageEntity.TEXT_MENTION:
                user_id = ent.user.id
                fst_name = ent.user.first_name

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

            elif ent.type == MessageEntity.MENTION:
                user_id = get_user_id(message.text[ent.offset:ent.offset +
                                                   ent.length])
                if not user_id:
                    # Should never happen, since for a user to become AFK they must have spoken. Maybe changed username?
                    return

                if user_id in chk_users:
                    return
                chk_users.append(user_id)

                try:
                    chat = context.bot.get_chat(user_id)
                except BadRequest:
                    print(f"Error: Could not fetch userid {user_id} for AFK module")
                    return
                fst_name = chat.first_name

            else:
                return

            check_afk(update, context, user_id, fst_name, userc_id)

    elif message.reply_to_message:
        user_id = message.reply_to_message.from_user.id
        fst_name = message.reply_to_message.from_user.first_name
        check_afk(update, context, user_id, fst_name, userc_id)


def check_afk(update, context, user_id, fst_name, userc_id):
    if is_user_afk(user_id):
        reason = afk_reason(user_id)
        since_afk = get_readable_time((time.time() - float(REDIS.get(f'afk_time_{user_id}'))))
        if int(userc_id) == int(user_id):
            return
        if reason == "none":
            res = "{} is Dead!\nLast Liveliness: {} ago".format(fst_name, since_afk)
        else:
            res = "{} is afk!\nReason: {}\nLast seen: {} ago".format(fst_name, reason, since_afk)

        update.effective_message.reply_text(res)

def __stats__():
    return f"𖣘 {len(REDIS.keys())} Registered keys in Redis Db."


def __user_info__(user_id):
    is_afk = is_user_afk(user_id)
    text = ""
    if is_afk:
        since_afk = get_readable_time((time.time() - float(REDIS.get(f'afk_time_{user_id}'))))
        text = "<i>This user is currently afk (away from keyboard).</i>"
        text += f"\n<i>Last Seen: {since_afk}</i>"
       
    else:
        text = "<i>This user currently isn't afk (not away from keyboard).</i>"
    return text


def __gdpr__(user_id):
    end_afk(user_id)

__help__ = """
 • /afk <reason>*:* mark yourself as AFK(away from keyboard).
 • brb <reason>*:* same as the afk command - but not a command.
When marked as AFK, any mentions will be replied to with a message to say you're not available!
"""
__mod_name__ = "AFK💤"

AFK_HANDLER = DisableAbleCommandHandler("afk", afk, run_async=True)
AFK_REGEX_HANDLER = MessageHandler(Filters.regex("(?i)brb"), afk, run_async=True)
NO_AFK_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups & ~Filters.update.edited_message, no_longer_afk, run_async=True)
AFK_REPLY_HANDLER = MessageHandler(Filters.all & Filters.chat_type.groups & ~Filters.update.edited_message, reply_afk, run_async=True)

dispatcher.add_handler(AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REGEX_HANDLER, AFK_GROUP)
dispatcher.add_handler(NO_AFK_HANDLER, AFK_GROUP)
dispatcher.add_handler(AFK_REPLY_HANDLER, AFK_REPLY_GROUP)
