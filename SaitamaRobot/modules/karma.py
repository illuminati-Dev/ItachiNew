import re
from pyrogram import filters, Client
from typing import Union, Dict
from SaitamaRobot import pbot as app, BOT_ID
from SaitamaRobot.utils.permissions import adminsOnly
from SaitamaRobot.modules.mongo.karma_mongo import (
    alpha_to_int,
    get_karma,
    get_karmas,
    int_to_alpha,
    is_karma_on,
    karma_off,
    karma_on,
    update_karma,
)
from SaitamaRobot.utils.filter_groups import karma_negative_group, karma_positive_group
from SaitamaRobot import aiohttpsession

regex_upvote = r"^((?i)\+|\+\+|\+1|thx|tnx|ty|thank you|thanx|thanks|pro|cool|good|👍|nice|noice|piro|Oho|oho|OwO|UwU|Nais|)$"
regex_downvote = r"^(\-|\-\-|\-1|👎|noob|Noob|gross|fuck off|Bhakk|Abe Saale|Tauba|Tauba Tauba Tuba Saara Mood Kharab Kardiya)$"

@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_upvote, re.IGNORECASE)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_positive_group,
)
async def upvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    karma = current_karma + 1 if current_karma else 1
    await update_karma(chat_id, await int_to_alpha(user_id), karma)
    await message.reply_text(
        f"Incremented Karma of {user_mention} By 1 \nTotal Points: {karma}"
    )

@app.on_message(
    filters.text
    & filters.group
    & filters.incoming
    & filters.reply
    & filters.regex(regex_downvote, re.IGNORECASE)
    & ~filters.via_bot
    & ~filters.bot,
    group=karma_negative_group,
)
async def downvote(_, message):
    if not await is_karma_on(message.chat.id):
        return
    if not message.reply_to_message.from_user:
        return
    if not message.from_user:
        return
    if message.reply_to_message.from_user.id == message.from_user.id:
        return

    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    user_mention = message.reply_to_message.from_user.mention
    current_karma = await get_karma(chat_id, await int_to_alpha(user_id))
    karma = current_karma - 1 if current_karma else -1
    await update_karma(chat_id, await int_to_alpha(user_id), karma)
    await message.reply_text(
        f"Decremented Karma Of {user_mention} By 1 \nTotal Points: {karma}"
    )

@app.on_message(filters.command("karma") & filters.group)
async def karma(_, message):
    chat_id = message.chat.id
    if not message.reply_to_message:
        m = await message.reply_text("Analyzing Karma...Will Take 10 Seconds")
        karma = await get_karmas(chat_id)
        if not karma:
            await m.edit("No karma in DB for this chat.")
            return
        msg = f"** ⚜️Top Karma Users list of {message.chat.title}📌 :- **\n"
        limit = 0
        karma_dicc = {}
        for i in karma:
            user_id = await alpha_to_int(i)
            user_karma = karma[i]["karma"]
            karma_dicc[str(user_id)] = user_karma
            karma_arranged = dict(
                sorted(karma_dicc.items(), key=lambda item: item[1], reverse=True)
            )
        if not karma_dicc:
            await m.edit("No karma in DB for this chat.")
            return
        for user_idd, karma_count in karma_arranged.items():
            if limit > 9:
                break
            try:
                user = await app.get_users(int(user_idd))
                await asyncio.sleep(0.8)
            except Exception:
                continue
            first_name = user.first_name
            if not first_name:
                continue
            username = user.username
            msg += f"\n✙ [{first_name[:12] + '...' if len(first_name) > 12 else first_name}](https://t.me/{username}) - **{karma_count}**"

            limit += 1
        await m.edit(msg, disable_web_page_preview=True)
    else:
        user_id = message.reply_to_message.from_user.id
        karma = await get_karma(chat_id, await int_to_alpha(user_id))
        karma = karma if karma else 0
        await message.reply_text(f"**Total Points**: __{karma}__")

@app.on_message(
    filters.command("karmas") & ~filters.private)
@adminsOnly("can_change_info")
async def captcha_state(_, message):
    usage = "**Usage:**\n/karmas [on|off]"
    if len(message.command) != 2:
        return await message.reply_text(usage)
    chat_id = message.chat.id
    state = message.text.split(None, 1)[1].strip()
    state = state.lower()
    if state == "on":
        await karma_on(chat_id)
        await message.reply_text("Enabled karma system.")
    elif state == "off":
        await karma_off(chat_id)
        await message.reply_text("Disabled karma system.")
    else:
        await message.reply_text(usage)

__help__ = """

❖ /karmas on/off :- Enables and disables karma in a chat **(Admin_only)**
❖ /karma  :- Lists Top 10 members of karma points in that specific chat.
❖ /karma (reply to a user_msg) :- Show karma points of that user.

"""

__mod_name__ = "Karma 👏"
