import requests

from pyrogram import filters
from pyrogram.types import (InlineKeyboardMarkup,
                            InlineKeyboardButton,
                            InlineQueryResultArticle,
                            InputTextMessageContent
                            )

from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot import pbot, telegraph, dispatcher
import SaitamaRobot.modules.sql.nsfw_sql as sql



@pbot.on_message(~filters.me & filters.command('nhentai', prefixes='/'), group=8)
async def nhentai(client, message):
    chat_id = message.chat.id
    if message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    query = message.text.split(" ")[1]

    title, tags, artist, total_pages, post_url, cover_image = nhentai_data(query)
    await message.reply_text(
        f"<code>{title}</code>\n\n<b>Tags:</b>\n{tags}\n<b>Artists:</b>\n{artist}\n<b>Pages:</b>\n{total_pages}",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        "Read Here",
                        url=post_url
                    )
                ]
            ]
        )
    )


def nhentai_data(noombers):
    url = f"https://nhentai.net/api/gallery/{noombers}"
    res = requests.get(url).json()
    pages = res["images"]["pages"]
    info = res["tags"]
    title = res["title"]["english"]
    links = []
    tags = ""
    artist = ''
    total_pages = res['num_pages']
    extensions = {
        'j':'jpg',
        'p':'png',
        'g':'gif'
    }
    for i, x in enumerate(pages):
        media_id = res["media_id"]
        temp = x['t']
        file = f"{i+1}.{extensions[temp]}"
        link = f"https://i.nhentai.net/galleries/{media_id}/{file}"
        links.append(link)

    for i in info:
        if i["type"] == "tag":
            tag = i['name']
            tag = tag.split(" ")
            tag = "_".join(tag)
            tags += f"#{tag} "
        if i["type"] == "artist":
            artist = f"{i['name']} "

    post_content = "".join(f"<img src={link}><br>" for link in links)

    post = telegraph.create_page(
        f"{title}",
        html_content=post_content,
        author_name="@Makima_UltraXBot", 
        author_url="https://t.me/Makima_UltraXBot"
    )
    return title,tags,artist,total_pages,post['url'],links[0]

__help__ = """
  • /nhentai [nhentai code] :- Gives telegraph view of that nhentai code comic

    nhentai code is a 6 digit code. It has unique codes for Unique doujins.
    U can try `/nhentai 261491`

  **⚠️Note :-** This cmd can be used in group if hentai is enable in the group.  To enable hentai use cmd /addhentai
"""   
__mod_name__ = "Nhentai📕"

NHENTAI_HANDLER = DisableAbleCommandHandler("nhentai", nhentai)

dispatcher.add_handler(NHENTAI_HANDLER)

__handlers__ = [
    NHENTAI_HANDLER,
]
