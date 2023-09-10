from asyncio import sleep
from SaitamaRobot.utlis.omdbs import get_movie_info
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from SaitamaRobot import pbot as Bot
from SaitamaRobot.utlis.db import get_collection
from SaitamaRobot.utlis.helper import control_user

DC = get_collection('DISABLED_CMDS')

               
@Bot.on_message(filters.command("imdb"))
@control_user
async def search(client, message, mdata: dict):
    find_gc = await DC.find_one({'_id': mdata['chat']['id']})
    if find_gc is not None and 'imdb' in find_gc['cmd_list'].split():
        return
    p = message.text.split(None, 1)[1]
    movie_name = p.replace(" ", "+")
    try:
        poster, id, text = get_movie_info(movie_name)
        buttons=[[InlineKeyboardButton('🎟 𝖨𝖬𝖣𝖻', url=f"https://www.imdb.com/title/{id}")]]    
        m=await message.reply_text("𝖥𝗂𝗇𝖽𝗂𝗇𝗀 𝖣𝖾𝗍𝖺𝗂𝗅𝗌..")
        await message.reply_photo(photo=poster.replace("SX300",""), caption=text, reply_markup=InlineKeyboardMarkup(buttons))
        await m.delete()                                                          
    except ValueError:
        m=await message.reply_text("𝖲𝗈𝗋𝗋𝗒,\n𝖨 𝖢𝖺𝗇'𝗍 𝖥𝗂𝗇𝖽 𝖯𝗈𝗌𝗍𝖾𝗋𝗌.\n𝖲𝖾𝗇𝖽𝗂𝗇𝗀 𝖠𝗏𝖺𝗂𝗅𝖺𝖻𝗅𝖾 𝖣𝖾𝗍𝖺𝗂𝗅𝗌..")
        await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
        await sleep(4)
        await m.delete()
    except Exception as e:
        buttons=[[InlineKeyboardButton('🔍 𝖲𝖾𝖺𝗋𝖼𝗁 𝖮𝗇 𝖦𝗈𝗈𝗀𝗅𝖾.', url=f'https://google.com/search?q={movie_name.replace(" ","+")}')]]
        await message.reply_text(text="𝖢𝗈𝗎𝗅𝖽𝗇'𝗍 𝖥𝖾𝗍𝖼𝗁 𝖣𝖾𝗍𝖺𝗂𝗅𝗌\n𝖳𝗋𝗒 𝖳𝗈 𝖢𝗁𝖾𝖼𝗄 yo𝗎𝗋 𝖲𝗉𝖾𝗅𝗅𝗂𝗇𝗀.", reply_markup=InlineKeyboardMarkup(buttons))  
        await m.delete()   
        print(e)

__help__ = """
❖/imdb (proper movie/sereis name) - Get a poster with the details of your movies/sereis query.

  **EXample -** /imdb Avengers
  
 **Note -** Name should be correct in the query otherwise it will return error.
  
"""    

__mod_name__ = "IMDB ♐"
