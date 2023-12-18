from datetime import datetime
from pyrogram import filters
from pyrogram.types import User, Message
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from SaitamaRobot import pbot

def ReplyCheck(message: Message):
    reply_id = None
    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id
    elif not message.from_user.is_self:
        reply_id = message.message_id
    return reply_id

infotext = (
    "**[{full_name}]({profile_link})**\n"
    " * UserID: `{user_id}`\n"
    " * First Name: `{first_name}`\n"
    " * Last Name: `{last_name}`\n"
    " * Username: `{username}`\n"
    " * Last Online: `{last_online}`\n"
    " * Bio: {bio}\n"
    " * Mutual Contacts: `{mutual_contacts}`"
)

def LastOnline(user: User):
    if user.is_bot:
        return ""
    elif user.status == 'recently':
        return "Recently"
    elif user.status == 'within_week':
        return "Within the last week"
    elif user.status == 'within_month':
        return "Within the last month"
    elif user.status == 'long_time_ago':
        return "A long time ago :("
    elif user.status == 'online':
        return "Currently Online"
    elif user.status == 'offline':
        return datetime.fromtimestamp(user.status.date).strftime("%a, %d %b %Y, %H:%M:%S")

def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name

@pbot.on_message(filters.command('whois'))
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except PeerIdInvalid:
        await message.reply("I don't know that User.")
        return
    desc = await client.get_chat(get_user)
    desc = desc.description
    user_photo = await client.get_profile_photos(user.id, limit=1)
    mutual_contacts = await client.get_users_mutual_contacts(user.id)

    profile_link = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"

    if user_photo:
        photo = user_photo[0]
        if photo.file_type == "video":
            # Handle video profile photo
            await message.reply_video(video=photo.file_id, caption=infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                bio=desc if desc else "`No bio set up.`",
                mutual_contacts=len(mutual_contacts),
                profile_link=profile_link
            ), disable_web_page_preview=True)
        else:
            # Handle regular photo
            await message.reply_photo(photo=photo.file_id, caption=infotext.format(
                full_name=FullName(user),
                user_id=user.id,
                first_name=user.first_name,
                last_name=user.last_name if user.last_name else "",
                username=user.username if user.username else "",
                last_online=LastOnline(user),
                bio=desc if desc else "`No bio set up.`",
                mutual_contacts=len(mutual_contacts),
                profile_link=profile_link
            ), disable_web_page_preview=True)
    else:
        # Handle case when there are no profile photos
        await message.reply_text(infotext.format(
            full_name=FullName(user),
            user_id=user.id,
            first_name=user.first_name,
            last_name=user.last_name if user.last_name else "",
            username=user.username if user.username else "",
            last_online=LastOnline(user),
            bio=desc if desc else "`No bio set up.`",
            mutual_contacts=len(mutual_contacts),
            profile_link=profile_link
        ), disable_web_page_preview=True)
