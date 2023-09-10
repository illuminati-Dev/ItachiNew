import io
import subprocess
import sys
from requests import post, get
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters
from SaitamaRobot import DEV_USERS, pbot as app
owner = DEV_USERS

def paste(text):
    url = "https://spaceb.in/api/v1/documents/"
    res = post(url, data={"content": text, "extension": "txt"})
    return f"https://spaceb.in/{res.json()['payload']['id']}"

@app.on_message(filters.command("logs") & filters.user(owner))
def semdlog(_, message):
    x = subprocess.getoutput("tail -100 log.txt")
    msg = "Makima logs here[⚙️](https://telegra.ph/file/92dc5cede0e3d7d5ebb2b.jpg)"
    message.reply_text(msg,
                       reply_markup=InlineKeyboardMarkup([[
                           InlineKeyboardButton("see🔧", url=paste(x)),
                           InlineKeyboardButton("Get file📎", callback_data="send")
                       ]]))
                       
                       
@app.on_callback_query(filters.regex("send") & filters.user(owner))
async def semdd(_, query):
    await query.message.edit("**Sent Logs as file**")
    await app.send_document(query.message.chat.id, "log.txt")
