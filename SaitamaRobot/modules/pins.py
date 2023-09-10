from asyncio import sleep
from html import escape
from os import remove
from traceback import format_exc

from pyrogram import filters
from pyrogram.errors import (
    ChatAdminInviteRequired,
    ChatAdminRequired,
    FloodWait,
    RightForbidden,
    RPCError,
    UserAdminInvalid,
)
from pyrogram.types import Message, ChatPrivileges

from SaitamaRobot import DEV_USERS, LOGGER, OWNER_ID, DRAGONS
import os 
from typing import Tuple

from SaitamaRobot import BOT_ID
from SaitamaRobot import pbot as app
from SaitamaRobot.utlis.permissions import adminsOnly


@app.on_message(
    filters.command(["pin", "unpin"]) & ~filters.private
)
@adminsOnly("can_pin_messages")
async def pin(_, message: Message):
    if not message.reply_to_message:
        return await message.reply_text("Reply to a message to pin/unpin it.")
    r = message.reply_to_message
    if message.command[0][0] == "u":
        await r.unpin()
        return await message.reply_text(
            f"**Unpinned [this]({r.link}) message.**",
            disable_web_page_preview=True,
        )
    await r.pin(disable_notification=True)
    await message.reply(
        f"**Pinned [this]({r.link}) message.**",
        disable_web_page_preview=True,
    )
    
