# Copyright 2023 Qewertyy <https://telegram.dog/Qewertyy>, MIT License
# SOURCE https://github.com/Team-ProjectCodeX
# PROVIDED BY https://t.me/ProjectCodeX

import requests
from pyrogram import filters, types
from SaitamaRobot import pbot as app

__mod_name__ = "Bard"
__help__ = """
- `/bard [prompt]`: Generate content based on the provided prompt using the Bard model.
"""

@app.on_message(filters.command("bard"))
async def bard(client, message):
    prompt = None
    if message.text is None:
        prompt = None
    if " " in message.text:
        try:
            return message.text.split(None, 1)[1]
        except IndexError:
            prompt = None
    else:
        prompt = None
    if prompt is None:
        return await message.reply_text("Hello, how can I assist you today?")
    resp = requests.post(
        f"https://lexica.qewertyy.me/models?model_id=20&prompt={prompt}"
    )
    if resp.status_code != 200:
        return await message.reply_text("An error occurred.")
    data = resp.json()
    try:
        text, images = data['content'], data['images']
        if len(images) == 0:
            await message.reply_text(text)
        else:
            media = []
            for i in images:
                media.append(types.InputMediaPhoto(i))
            media[0] = types.InputMediaPhoto(images[0], caption=text)
            await app.send_media_group(
                message.chat.id,
                media,
                reply_to_message_id=message.id
            )
    except Exception as Ok:
        print(Ok, data)
