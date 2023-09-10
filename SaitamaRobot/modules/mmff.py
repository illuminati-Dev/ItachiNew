from PIL import Image, ImageDraw, ImageEnhance, ImageFont, ImageOps
import textwrap
import os
from telethon import events
from telethon.tl.types import DocumentAttributeFilename
from telethon import functions, types
from SaitamaRobot.events import register
from SaitamaRobot import TEMP_DOWNLOAD_DIRECTORY
# how a lazy guy ports.
@register(pattern="^/mmf( (.*)|$)")
async def mmf(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await event.reply("reply to a sticker/image with meme text")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await event.reply("```Reply to a image/sticker.```")
        return
    file = await event.client.download_media(reply_message, TEMP_DOWNLOAD_DIRECTORY)
    msg = await event.reply("Memifying...")
    text = str(event.pattern_match.group(1)).strip()
    if not text:
        return await event.reply("You might want to try `/mmf` relpy sticker/image <text>")
    meme = await add_text_img(file, text)
    await event.client.send_file(event.chat_id, file=meme, force_document=False)
    await msg.delete()
    os.remove(meme)
    os.remove(file)

async def add_text_img(image_path, text):
    font_size = 14
    stroke_width = 2

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    font = ImageFont.truetype(
        font="SaitamaRobot/resources/MutantAcademyStyle.ttf",
        size=int(image_height * font_size) // 100,
    )
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    if top_lines:
        y = 10
        for line in top_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    if bottom_lines:
        y = image_height - char_height * len(bottom_lines) - 15
        for line in bottom_lines:
            line_width, line_height = font.getsize(line)
            x = (image_width - line_width) / 2
            draw.text(
                (x, y),
                line,
                fill="white",
                font=font,
                stroke_width=stroke_width,
                stroke_fill="black",
            )
            y += line_height

    final_image = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "memify.webp")
    img.save(final_image, **img_info)
    return final_image

