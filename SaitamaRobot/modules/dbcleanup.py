from time import sleep
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler, run_async)
from SaitamaRobot import DEV_USERS, OWNER_ID, dispatcher
from SaitamaRobot.modules.helper_funcs.chat_status import dev_plus
import SaitamaRobot.modules.sql.global_bans_sql as gban_sql
import SaitamaRobot.modules.sql.users_sql as user_sql

def get_invalid_chats(update: Update, context: CallbackContext, remove: bool = False):
    bot = context.bot
    chat_id = update.effective_chat.id
    chats = user_sql.get_all_chats()
    kicked_chats, progress = 0, 0
    chat_list = []
    progress_message = None

    for progress, chat in enumerate(chats):
        try:
            bot.get_chat(chat.chat_id, timeout=60)
        except (BadRequest, Unauthorized):
            kicked_chats += 1
            chat_list.append(chat.chat_id)

    if remove:
        for kicked_chat in chat_list:
            user_sql.rem_chat(kicked_chat)
            sleep(0.1)

    return kicked_chats


def get_invalid_gban(update: Update, context: CallbackContext, remove: bool = False):
    bot = context.bot
    banned = gban_sql.get_gban_list()
    ungbanned_users = 0
    ungban_list = []

    for user in banned:
        user_id = user["user_id"]
        sleep(0.1)
        try:
            bot.get_chat(user_id)
        except BadRequest:
            ungbanned_users += 1
            ungban_list.append(user_id)

    if remove:
        for user_id in ungban_list:
            gban_sql.ungban_user(user_id)
            sleep(0.1)

    return ungbanned_users


@dev_plus
def dbcleanup(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat_id = msg.chat_id

    msg.reply_text("Calculating the number of invalid chats...")
    invalid_chat_count = get_invalid_chats(update, context)

    msg.reply_text("Calculating the number of invalid gbanned users...")
    invalid_gban_count = get_invalid_gban(update, context)

    reply = f"Total invalid chats: {invalid_chat_count}\n"
    reply += f"Total invalid gbanned users: {invalid_gban_count}"

    buttons = [[InlineKeyboardButton("Cleanup DB", callback_data="db_cleanup")]]

    update.effective_message.reply_text(
        reply, reply_markup=InlineKeyboardMarkup(buttons)
    )


def callback_button(update: Update, context: CallbackContext):
    bot = context.bot
    query = update.callback_query
    message = query.message
    chat_id = update.effective_chat.id
    query_type = query.data

    admin_list = [OWNER_ID] + DEV_USERS

    bot.answer_callback_query(query.id)

    if query_type == "db_leave_chat" and query.from_user.id in admin_list:
        bot.edit_message_text("Leaving chats...", chat_id, message.message_id)
        chat_count = get_invalid_chats(update, context, True)
        bot.send_message(chat_id, f"Left {chat_count} chats.")
    elif (
        query_type == "db_leave_chat"
        or query_type == "db_cleanup"
        and query.from_user.id not in admin_list
    ):
        query.answer("You are not allowed to use this.")
    elif query_type == "db_cleanup":
        bot.edit_message_text("Cleaning up DB...", chat_id, message.message_id)
        invalid_chat_count = get_invalid_chats(update, context, True)
        invalid_gban_count = get_invalid_gban(update, context, True)
        reply = f"Cleaned up {invalid_chat_count} chats and {invalid_gban_count} gbanned users from the database."

        bot.send_message(chat_id, reply)


DB_CLEANUP_HANDLER = CommandHandler("dbcleanup", dbcleanup, run_async=True)
BUTTON_HANDLER = CallbackQueryHandler(
    callback_button, pattern='db_.*', run_async=True
)

dispatcher.add_handler(DB_CLEANUP_HANDLER)
dispatcher.add_handler(BUTTON_HANDLER)

__mod_name__ = "DB Cleanup"
__handlers__ = [DB_CLEANUP_HANDLER, BUTTON_HANDLER]
