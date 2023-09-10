from SaitamaRobot.events import register
from SaitamaRobot import OWNER_ID
from SaitamaRobot import telethn as tbot
import os 
from PIL import Image, ImageDraw, ImageFont


@register(pattern="/blogo( (.*)|$)")
async def lego(event):
 quew = event.pattern_match.group(1)
 if event.sender_id != OWNER_ID and not quew:
  await event.reply('Provide Some Text To Draw!')
  return
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./SaitamaRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./SaitamaRobot/resources/Chopsic.otf", 330)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_width-w)/2, (image_height-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_width-w)/2
    y= ((image_height-h)/2+6)
    draw.text((x, y), text, font=font, fill="black", stroke_width=25, stroke_fill="yellow")
    fname2 = "Logo_By_Makima.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="✌️✨Made By @Makima_UltraXBot ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @makima_bot_support, {e}')



   
@register(pattern="/wlogo( (.*)|$)")
async def lego_(event):
 quew = event.pattern_match.group(1)
 if event.sender_id != OWNER_ID and not quew:
  await event.reply('Provide Some Text To Draw!')
  return
 await event.reply('Creating your logo...wait!')
 try:
    text = event.pattern_match.group(1)
    img = Image.open('./SaitamaRobot/resources/blackbg.jpg')
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("./SaitamaRobot/resources/Maghrib.ttf", 1000)
    w, h = draw.textsize(text, font=font)
    h += int(h*0.21)
    image_width, image_height = img.size
    draw.text(((image_width-w)/2, (image_height-h)/2), text, font=font, fill=(255, 255, 255))
    x = (image_width-w)/2
    y= ((image_height-h)/2+6)
    draw.text((x, y), text, font=font, fill="white", stroke_width=0, stroke_fill="white")
    fname2 = "Logo_By_Makima.png"
    img.save(fname2, "png")
    await tbot.send_file(event.chat_id, fname2, caption="✌️✨Made By @Makima_UltraXBot ❤️")
    if os.path.exists(fname2):
            os.remove(fname2)
 except Exception as e:
   await event.reply(f'Error Report @Makima_Bot_Support, {e}')

file_help = os.path.basename(__file__)
file_help = file_help.replace(".py", "")
file_helpo = file_help.replace("_", " ")


__help__ = """
 ❍ /logo text :  Create your logo with your text [Anime Backround]
 ❍ /blogo text :  Create your logo with your text [Black Backround]
 ❍ /wlogo text :  Create your logo with your text [Black Backround  ,White Text]


 """
__mod_name__ = "Logo💞"



