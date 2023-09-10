from requests import request
from SaitamaRobot import pbot as app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import filters

key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="See Language Codes",
                                url=f"https://telegra.ph/Lang-Codes-03-19-3",
                            )
                        ],
                    ]
                )


@app.on_message(filters.command("tr"))
async def tr(_, message):
    if len(message.command) != 2:
        lang = "en"
    else:
        lang = message.text.split(None, 1)[1]
    if not message.reply_to_message:
        return await message.reply_text(
            "Reply to a message with /tr "
            + "\nor reply a text with /tr [langauage_code] ex:- /tr hi , for hindi transalation."
            + "\n\nSee Below button for language codes list.",
            reply_markup=key,
        )
    reply = message.reply_to_message
    text = reply.text or reply.caption
    if not text:
        return await message.reply_text("Reply to a text to translate it")
    url = f"https://arq.hamker.dev/translate?text={text}&destLangCode={lang}"
    headers = {
        "accept": "application/json",
        "X-API-KEY": "PDQVNR-HVFFFP-ZGVHUS-ZHWPFH-ARQ",
    }
    response = request("GET", url, headers=headers)
    p = response.json()
    k = p["ok"]
    r = p["result"]
    if not k:
        return await message.reply_text(r)
    des = p["result"]["dest"]
    src = p["result"]["src"]
    trtext = p["result"]["translatedText"]
    await message.reply_text(f"Translated from {src} to {des}: {trtext}")
    
    
__help__ = """ 
Use this module to translate stuff!
*Commands:*
   ➢ tr {language_code} (or only /tr): as a reply to a message, translates it to language code given or English will be default.
   
eg: /tr ja (as reply to a message): translates to Japanese.
• [List of supported languages for translation](https://telegra.ph/Lang-Codes-03-19-3)
"""

__mod_name__ = "Translator"
