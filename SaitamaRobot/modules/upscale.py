# Created by: t.me/AlphaXCoder

import requests
from PIL import Image
from io import BytesIO
import os
import base64
from pyrogram import *
from SaitamaRobot import pbot as app

__mod_name__ = "Upscaler"
__help__ = """
- `/upscale`: Reply to an image to upscale it.
"""

@app.on_message(filters.command("upscale"))
async def upscale(client, message):
    try:
        image = await message.reply_to_message.download()
    except:
        return await message.reply_text("Reply to an image to upscale images.")
    temp = await message.reply_text("**Wait a moment, upscaling your image....**")
    with open(image, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())
    img = encoded_image.decode('utf-8')
    response = requests.post("https://alphacoder-api.vercel.app/v2/upscale", json={"image": img})
    try:
        link = response.json()["image_url"]
        resp = requests.get(link)
        data = resp.content
        Img = Image.open(BytesIO(data))
        Img.save("upscale.png")
        await message.reply_document("upscale.png")
        await temp.delete()
        os.remove("upscale.png")
    except:
        return await temp.edit_text("**Try again after 10 seconds.**")
