import html
import os
from telegram import Update
from telegram.ext import CallbackContext, CommandHandler, MessageHandler, Filters
from SaitamaRobot.modules.helper_funcs.decorators import makicmd, makimsg
from SaitamaRobot.modules.helper_funcs.anonymous import user_admin, AdminPerms
from SaitamaRobot.modules.mongo.antichannelmongo import antichannel_status, disable_antichannel, enable_antichannel

# Command handler for /antichannel command
@makicmd(command="antichannel", group=100)
@user_admin(AdminPerms.CAN_RESTRICT_MEMBERS)
def set_antichannel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat

    if chat.type == "private":
        return

    args = context.args
    if args:
        s = args[0].lower()
        if s in ["yes", "on"]:
            enable_antichannel(chat.id)
            message.reply_html(f"Enabled antichannel in {html.escape(chat.title)}")
        elif s in ["off", "no"]:
            disable_antichannel(chat.id)
            message.reply_html(f"Disabled antichannel in {html.escape(chat.title)}")
        else:
            message.reply_text(f"Unrecognized argument: {s}")
    else:
        message.reply_html(
            f"Antichannel setting is currently {'enabled' if antichannel_status(chat.id) else 'disabled'} in {html.escape(chat.title)}"
        )

# Message handler to eliminate messages from channels in anti-channel-enabled chats
@makimsg(Filters.chat_type.groups, group=110)
def eliminate_channel(update: Update, context: CallbackContext):
    message = update.effective_message
    chat = update.effective_chat
    bot = context.bot

    if antichannel_status(chat.id) and message.sender_chat and message.sender_chat.type == "channel" and not message.is_automatic_forward:
        message.delete()
        sender_chat = message.sender_chat
        bot.ban_chat_sender_chat(sender_chat_id=sender_chat.id, chat_id=chat.id)

# Help and module name information
__help__ = """
**Admin command:**

❖ /antichannel (on/yes/off/no) - After enabling this, it will ban and delete channel user messages.

**If you want to ban only a specific channel, reply to that channel with /ban, and to unban it, reply /unban.**
"""

__mod_name__ = "Antichannel❌"
