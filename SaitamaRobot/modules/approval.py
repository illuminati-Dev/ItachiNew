import html
from telegram import Chat, User, ParseMode
from telegram.error import BadRequest
from telegram.utils.helpers import mention_html
from telegram import Bot, Update
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler, Filters, run_async
from telegram import InlineKeyboardMarkup, InlineKeyboardButton

import SaitamaRobot.modules.sql.approve_sql as sql
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot import dispatcher, DRAGONS
from SaitamaRobot.modules.helper_funcs.chat_status import user_admin

from SaitamaRobot.modules.helper_funcs.extraction import extract_user
from SaitamaRobot.modules.helper_funcs.alternate import typing_action




@typing_action
def approval(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    chat = update.effective_chat
    args = context.args
    user_id = extract_user(message, args)
    member = chat.get_member(int(user_id))
    if not user_id:
        message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!",
        )
        return ""
    if sql.is_approved(message.chat_id, user_id):
        message.reply_text(
            f"{member.user['first_name']} is an approved user. Locks, antiflood, and blocklists won't apply to them.",
        )
    else:
        message.reply_text(
            f"{member.user['first_name']} is not an approved user. They are affected by normal commands.",
        )



@user_admin
@typing_action
def approve(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!",
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status in ("administrator", "creator"):
        message.reply_text(
            "User is already admin - locks, blocklists, and antiflood already don't apply to them.",
        )
        return ""
    if sql.is_approved(message.chat_id, user_id):
        message.reply_text(
            f"[{member.user['first_name']}](tg://user?id={member.user['id']}) is already approved in {chat_title}",
            parse_mode=ParseMode.MARKDOWN,
        )
        return ""
    sql.approve(message.chat_id, user_id)
    message.reply_text(
        f"[{member.user['first_name']}](tg://user?id={member.user['id']}) has been approved in {chat_title}! They will now be ignored by automated admin actions like locks, blocklists, and antiflood.",
        parse_mode=ParseMode.MARKDOWN,
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#APPROVED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message



@user_admin
@typing_action
def unapprove(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    args = context.args
    user = update.effective_user
    user_id = extract_user(message, args)
    if not user_id:
        message.reply_text(
            "I don't know who you're talking about, you're going to need to specify a user!",
        )
        return ""
    try:
        member = chat.get_member(user_id)
    except BadRequest:
        return ""
    if member.status in ("administrator", "creator"):
        message.reply_text("This user is an admin, they can't be unapproved.")
        return ""
    if not sql.is_approved(message.chat_id, user_id):
        message.reply_text(f"{member.user['first_name']} isn't approved yet!")
        return ""
    sql.disapprove(message.chat_id, user_id)
    message.reply_text(
        f"{member.user['first_name']} is no longer approved in {chat_title}.",
    )
    log_message = (
        f"<b>{html.escape(chat.title)}:</b>\n"
        f"#UNAPPROVED\n"
        f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
        f"<b>User:</b> {mention_html(member.user.id, member.user.first_name)}"
    )

    return log_message


@user_admin
@typing_action
def approved(update: Update, context: CallbackContext) -> str:
    message = update.effective_message
    chat_title = message.chat.title
    chat = update.effective_chat
    msg = "The following users are approved.\n"
    approved_users = sql.list_approved(message.chat_id)
    for i in approved_users:
        member = chat.get_member(int(i.user_id))
        msg += f"- `{i.user_id}`: {member.user['first_name']}\n"
    if msg.endswith("approved.\n"):
        message.reply_text(f"No users are approved in {chat_title}.")
        return ""
    message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)

@user_admin
@typing_action
def unapproveall(update, context):
    chat = update.effective_chat
    user = update.effective_user
    member = chat.get_member(user.id)
    if member.status != "creator" and user.id not in DRAGONS:
        update.effective_message.reply_text(
            "Only the chat owner can unapprove all users at once.",
        )
    else:
        buttons = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Unapprove all users",
                        callback_data="unapproveall_user",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Cancel",
                        callback_data="unapproveall_cancel",
                    ),
                ],
            ],
        )
        update.effective_message.reply_text(
            f"Are you sure you would like to unapprove ALL users in {chat.title}? This action cannot be undone.",
            reply_markup=buttons,
            parse_mode=ParseMode.MARKDOWN,
        )

@user_admin
@typing_action
def unapproveall_btn(update: Update, context: CallbackContext):
    query = update.callback_query
    chat = update.effective_chat
    message = update.effective_message
    member = chat.get_member(query.from_user.id)
    if query.data == "unapproveall_user":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            approved_users = sql.list_approved(chat.id)
            users = [int(i.user_id) for i in approved_users]
            for user_id in users:
                sql.disapprove(chat.id, user_id)
            message.edit_text("Successfully Unapproved all user in this Chat.")
            return

        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")

        if member.status == "member":
            query.answer("You need to be admin to do this.")
    elif query.data == "unapproveall_cancel":
        if member.status == "creator" or query.from_user.id in DRAGONS:
            message.edit_text("Removing of all approved users has been cancelled.")
            return ""
        if member.status == "administrator":
            query.answer("Only owner of the chat can do this.")
        if member.status == "member":
            query.answer("You need to be admin to do this.")


__mod_name__ = "Approval✅"    

__help__ = """ 
\
Sometimes, you might trust a user not to send unwanted content.
Maybe not enough to make them admin, but you might be ok with locks, blacklists, and antiflood not applying to them.
That's what approvals are for - approve of trustworthy users to allow them to send
*Admin commands:*
❂ /approval*:* Check a user's approval status in this chat.
❂ /approve*:* Approve of a user. Locks, blacklists, and antiflood won't apply to them anymore.
❂ /unapprove*:* Unapprove of a user. They will now be subject to locks, blacklists, and antiflood again.
❂ /approved*:* List all approved users.
❂ /unapproveall*:* Unapprove *ALL* users in a chat. This cannot be undone.
\
"""    

APPROVED_HANDLER = DisableAbleCommandHandler("approved", approved, filters=Filters.chat_type.groups, run_async=True)
UNAPPROVE_ALL_HANDLER = DisableAbleCommandHandler("unapproveall", unapproveall, filters=Filters.chat_type.groups, run_async=True)
APPROVE_HANDLER = DisableAbleCommandHandler("approve", approve, pass_args=True, filters=Filters.chat_type.groups, run_async=True)
UNAPPROVE_HANDLER = DisableAbleCommandHandler("unapprove", unapprove, pass_args=True, filters=Filters.chat_type.groups, run_async=True)
APPROVEL_HANDLER = DisableAbleCommandHandler("approval", approval, pass_args=True, filters=Filters.chat_type.groups, run_async=True)
UNAPPROVEALL_BTN = CallbackQueryHandler(
    unapproveall_btn, pattern=r"unapproveall_.*", run_async=True)


dispatcher.add_handler(APPROVED_HANDLER)
dispatcher.add_handler(UNAPPROVE_ALL_HANDLER)
dispatcher.add_handler(APPROVE_HANDLER) 
dispatcher.add_handler(UNAPPROVE_HANDLER) 
dispatcher.add_handler(APPROVEL_HANDLER)
dispatcher.add_handler(UNAPPROVEALL_BTN)
