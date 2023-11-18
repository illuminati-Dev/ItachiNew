from PIL import Image, ImageDraw, ImageFont
import textwrap
import os
from pyrogram import filters
from SaitamaRobot import TEMP_DOWNLOAD_DIRECTORY
from SaitamaRobot import pbot as app

# Load a font that supports getsize
font_path = "SaitamaRobot/resources/American Captain.ttf"
font_size = 14
font = ImageFont.truetype(font_path, size=font_size)

@app.on_message(filters.command("mmf") & filters.reply)
async def mmf_func(_, message):
    if not message.reply_to_message:
        await message.reply("Reply to a sticker/image with meme text.")
        return

    reply_message = message.reply_to_message
    if not reply_message.media:
        await message.reply("Reply to an image/sticker.")
        return

    file = await app.download_media(reply_message)
    msg = await message.reply("Memifying...")

    text = message.text.split(" ", 1)[1].strip()
    if not text:
        return await message.reply("You might want to try `/mmf` reply to sticker/image <text>")

    meme = await add_text_img(file, text)
    await app.send_document(message.chat.id, document=meme)
    await msg.delete()
    os.remove(meme)
    os.remove(file)

async def add_text_img(image_path, text):
    stroke_width = 2

    if ";" in text:
        upper_text, lower_text = text.split(";")
    else:
        upper_text = text
        lower_text = ""

    img = Image.open(image_path).convert("RGBA")
    img_info = img.info
    image_width, image_height = img.size
    draw = ImageDraw.Draw(img)

    char_width, char_height = font.getsize("A")
    chars_per_line = image_width // char_width
    top_lines = textwrap.wrap(upper_text, width=chars_per_line)
    bottom_lines = textwrap.wrap(lower_text, width=chars_per_line)

    draw_text_lines(draw, top_lines, char_height, image_width, stroke_width, "white", "black")
    draw_text_lines(draw, bottom_lines, image_height, image_width, stroke_width, "white", "black", bottom=True)

    final_image = os.path.join(TEMP_DOWNLOAD_DIRECTORY, "memify.webp")
    img.save(final_image, **img_info)
    return final_image

def draw_text_lines(draw, lines, y, image_width, stroke_width, text_fill, stroke_fill, bottom=False):
    for line in lines:
        line_width, line_height = font.getsize(line)
        x = (image_width - line_width) / 2
        if bottom:
            y -= line_height
        draw.text(
            (x, y),
            line,
            fill=text_fill,
            font=font,
            stroke_width=stroke_width,
            stroke_fill=stroke_fill,
        )
        if not bottom:
            y += line_height

__help__ = """
*Commands:* 
• /mmf: Add text to a sticker or image and create a meme.
Reports bugs at @UchihaPolice_Support
"""

__mod_name__ = "Meme Maker 🃏"
