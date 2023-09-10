import os
import io
import random
import glob
import requests
from pymongo import MongoClient as m
from SaitamaRobot.events import register
from telethon.tl.types import InputMessagesFilterPhotos
from SaitamaRobot import telethn as tbot
from PIL import Image, ImageDraw, ImageFont
from requests import get


def mediainfo(media):
    xx = str((str(media)).split("(", maxsplit=1)[0])
    m = ""
    if xx == "MessageMediaDocument":
        mim = media.document.mime_type
        if mim == "application/x-tgsticker":
            m = "sticker animated"
        elif "image" in mim:
            if mim == "image/webp":
                m = "sticker"
            elif mim == "image/gif":
                m = "gif as doc"
            else:
                m = "pic as doc"
        elif "video" in mim:
            if "DocumentAttributeAnimated" in str(media):
                m = "gif"
            elif "DocumentAttributeVideo" in str(media):
                i = str(media.document.attributes[0])
                if "supports_streaming=True" in i:
                    m = "video"
                m = "video as doc"
            else:
                m = "video"
        elif "audio" in mim:
            m = "audio"
        else:
            m = "document"
    elif xx == "MessageMediaPhoto":
        m = "pic"
    elif xx == "MessageMediaWebPage":
        m = "web"
    return m


@register(pattern="/logo( (.*)|$)")
async def lego(event):
    quew = event.pattern_match.group(1)
    if not quew:
        await event.reply('Please Give A Text For The Logo.')
        return
    pesan = await event.reply('Making your Logo. Kindly Wait.')
    try:
        text = event.pattern_match.group(1)
        x = m(
            'mongodb+srv://animeapi:animeapi@cluster0.7papd0m.mongodb.net/?retryWrites=true&w=majority')['logo']['Logo']
        u = x.find()
        randc = random.choice([m['url'] for m in u])
        if event.reply_to_msg_id:
            temp = await event.get_reply_message()
            if temp.media.photo:
               ig = await temp.download_media()
        else:
            ig = io.BytesIO(requests.get(randc).content)
        img = Image.open(ig)
        draw = ImageDraw.Draw(img)
        image_widthz, image_heightz = img.size
        pointsize = 500
        fillcolor = "black"
        shadowcolor = "blue"
        fnt = glob.glob("./SaitamaRobot/resources/Logo/*")
        randf = random.choice(fnt)
        font = ImageFont.truetype(randf, 120)
        w, h = draw.textsize(text, font=font)
        h += int(h*0.21)
        image_width, image_height = img.size
        draw.text(((image_widthz-w)/2, (image_heightz-h)/2),
                      text, font=font, fill=(255, 255, 255))
        x = (image_widthz-w)/2
        y = ((image_heightz-h)/2+6)
        draw.text((x, y), text, font=font, fill="white",
                      stroke_width=1, stroke_fill="black")
        fname = "MakimaLogo.png"
        img.save(fname, "png")
        await tbot.send_file(event.chat_id, file=fname, caption=f"✌️✨Made By @Makima_UltraXBot ❤️")
        await pesan.delete()
        if os.path.exists(fname):
           os.remove(fname)
    except Exception as e:
        await event.reply(f'Error, Report @Makima_Bot_Support, {e}')
