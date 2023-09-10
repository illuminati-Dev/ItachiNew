from io import BytesIO
from traceback import format_exc

from aiohttp import ClientSession
from pyrogram import filters
from pyrogram.types import Message
from Python_ARQ import ARQ

from SaitamaRobot import pbot as app

aiohttpsession = ClientSession()
ARQ_API_KEY = "QQEGEK-ZYQIEP-BWAKDM-UJFKPZ-ARQ"
ARQ_API_URL = "http://arq.hamker.dev"
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)


async def quotify(messages: list):
    response = await arq.quotly(messages)
    if not response.ok:
        return [False, response.result]
    sticker = response.result
    sticker = BytesIO(sticker)
    sticker.name = "sticker.webp"
    return [True, sticker]


def getArg(message: Message) -> str:
    arg = message.text.strip().split(None, 1)[1].strip()
    return arg


def isArgInt(message: Message) -> bool:
    count = getArg(message)
    try:
        count = int(count)
        return [True, count]
    except ValueError:
        return [False, 0]


@app.on_message(filters.command("q"))
async def quotly_func(_, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Reply to a message to quote it.")
        return
    if not message.reply_to_message.text:
        await message.reply_text("Replied message has no text, can't quote it.")
        return
    m = await message.reply_text("Quoting Messages")
    if len(message.command) < 2:
        messages = [message.reply_to_message]

    elif len(message.command) == 2:
        arg = isArgInt(message)
        if arg[0]:
            if arg[1] < 2 or arg[1] > 10:
                await m.edit("Argument must be between 2-10.")
                return
            count = arg[1]
            messages = await app.get_messages(
                message.chat.id,
                list(
                    range(
                        message.reply_to_message.message_id,
                        message.reply_to_message.message_id + count,
                    )
                ),
                replies=0,
            )
        else:
            if getArg(message) != "r":
                await m.edit(
                    "Incorrect Argument, Pass **'r'** or **'INT'**, **EX:** __/q 2__"
                )
                return
            reply_message = await app.get_messages(
                message.chat.id,
                message.reply_to_message.message_id,
                replies=1,
            )
            messages = [reply_message]
    else:
        await m.edit("Incorrect argument, check quotly module in help section.")
        return
    try:
        sticker = await quotify(messages)
        if not sticker[0]:
            await message.rely_text(sticker[1])
            await m.delete()
            return
        sticker = sticker[1]
        await message.reply_sticker(sticker)
        await m.delete()
        sticker.close()
    except Exception as e:
        await message.reply_text(
            "Something wrong happened while quoting messages,"
            + " This error usually happens when there's a "
            + " message containing something other than text."
        )
        await m.delete()
        e = format_exc()
        print(e)
        return

'''
_help = """
Here is the help for **Quotly**:

**Command for anyone**
**->** `/q`: makes beautiful quotes of the messages.
**->** `/quote`: alias of q ~
**->** `/qrate <on/off>`: Toggle quote rating buttons.
**->** `/qtop`: Preview the top quotes of the chat.
**->** `/qrand`: show random quotes of the chat 

**Examples**
**-** `/q red r 2 p`: makes quote in red color, includes reply, and collects 2 messages in between and sends as photo.
"""

help.update({"quotly": _help})
'''
