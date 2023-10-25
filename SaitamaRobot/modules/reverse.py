import os
import re
import requests
import urllib
import urllib.request
import urllib.parse
from urllib.error import URLError, HTTPError
from bs4 import BeautifulSoup
from pyrogram import filters
from pyrogram.types import InputMediaPhoto
from pyrogram.errors import TelegramError
from SaitamaRobot import pbot as app

opener = urllib.request.build_opener()
useragent = 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'
opener.addheaders = [('User-agent', useragent)]

@app.on_message(filters.command("reverse") | filters.command("grs") | filters.command("pp"))
async def reverse(_, message):
    if os.path.isfile("okgoogle.png"):
        os.remove("okgoogle.png")

    chat_id = message.chat.id
    rtmid = message.message_id
    imagename = "okgoogle.png"

    reply = message.reply_to_message
    if reply:
        if reply.sticker:
            file_id = reply.sticker.file_id
        elif reply.photo:
            file_id = reply.photo[-1].file_id
        elif reply.document:
            file_id = reply.document.file_id
        else:
            await message.reply_text("Reply to an image or sticker to look it up.")
            return
        image_file = await app.get_file(file_id)
        await image_file.download(imagename)
    elif message.command:
        splatargs = message.text.split(" ")
        if len(splatargs) == 3:
            img_link = splatargs[1]
            try:
                lim = int(splatargs[2])
            except:
                lim = 2
        elif len(splatargs) == 2:
            img_link = splatargs[1]
            lim = 2
        else:
            await message.reply_text("/reverse <link> <amount of images to return>")
            return
        try:
            urllib.request.urlretrieve(img_link, imagename)
        except HTTPError as HE:
            if HE.reason == 'Not Found':
                await message.reply_text("Image not found.")
                return
            elif HE.reason == 'Forbidden':
                await message.reply_text("Couldn't access the provided link. The website might have blocked access by the bot or the website does not exist.")
                return
        except URLError as UE:
            await message.reply_text(f"{UE.reason}")
            return
        except ValueError as VE:
            await message.reply_text(f"{VE}\nPlease try again using http or https protocol.")
            return
    else:
        await message.reply_markdown("Please reply to a sticker or an image to search it. You can also search an image with a link using `/reverse [picturelink] <amount>`.")
        return

    try:
        searchUrl = 'https://www.google.com/searchbyimage/upload'
        multipart = {'encoded_image': (imagename, open(imagename, 'rb')), 'image_content': ''}
        response = requests.post(searchUrl, files=multipart, allow_redirects=False)
        fetchUrl = response.headers['Location']

        if response.status_code != 400:
            xx = await app.send_message(chat_id, "Image was successfully uploaded to Google. Parsing it, please wait.", reply_to_message_id=rtmid)
        else:
            xx = await app.send_message(chat_id, "Google told me to go away.", reply_to_message_id=rtmid)
            return

        os.remove(imagename)
        match = ParseSauce(fetchUrl + "&hl=en")
        guess = match['best_guess']
        if match['override'] and not match['override'] == '':
            imgspage = match['override']
        else:
            imgspage = match['similar_images']

        if guess and imgspage:
            await xx.edit_text(f"[{guess}]({fetchUrl})\nProcessing...", parse_mode='markdown', disable_web_page_preview=True)
        else:
            await xx.edit_text("Couldn't find anything.")
            return

        images = scam(imgspage, lim)
        if len(images) == 0:
            await xx.edit_text(f"[{guess}]({fetchUrl})\n[Visually similar images]({imgspage})\nCouldn't fetch any images.", parse_mode='markdown', disable_web_page_preview=True)
            return

        imglinks = []
        for link in images:
            lmao = InputMediaPhoto(media=str(link))
            imglinks.append(lmao)

        await app.send_media_group(chat_id=chat_id, media=imglinks, reply_to_message_id=rtmid)
        await xx.edit_text(f"[{guess}]({fetchUrl})\n[Visually similar images]({imgspage})", parse_mode='markdown', disable_web_page_preview=True)
    except TelegramError as e:
        print(e)
    except Exception as exception:
        print(exception)

__help__ = """
*Commands:* 
• /reverse | pp | grs: Does a reverse image search of the media which it was replied to.
Reports bugs at @UchihaPolice_Support
"""

__mod_name__ = "Reverse"
