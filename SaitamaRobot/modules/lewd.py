import os
import html
import hmtai
import requests
from PIL import Image
from telegram import ParseMode
from SaitamaRobot import dispatcher, updater
import SaitamaRobot.modules.sql.nsfw_sql as sql
from SaitamaRobot.modules.log_channel import gloggable
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram.error import BadRequest, RetryAfter, Unauthorized
from telegram.ext import CommandHandler, run_async, CallbackContext
from SaitamaRobot.modules.helper_funcs.filters import CustomFilters
from SaitamaRobot.modules.helper_funcs.chat_status import user_admin
from telegram.utils.helpers import mention_html, mention_markdown, escape_markdown

@user_admin
@gloggable
def add_hentai(update: Update, context: CallbackContext):
    chat = update.effective_chat
    msg = update.effective_message
    user = update.effective_user #Remodified by @EverythingSuckz
    is_hentai = sql.is_hentai(chat.id)
    if msg.chat.type == "private":
        msg.reply_text("🙂 this command is only for groups. You can use hentai/nsfw commands here without enabling hentai")
    elif not is_hentai:
        sql.set_hentai(chat.id)
        msg.reply_text("Activated hentai Mode!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"ACTIVATED_hentai\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message
    else:
        msg.reply_text("hentai Mode is already Activated for this chat!")
        return ""



@user_admin
@gloggable
def rem_hentai(update: Update, context: CallbackContext):
    msg = update.effective_message
    chat = update.effective_chat
    user = update.effective_user
    is_hentai = sql.is_hentai(chat.id)
    if msg.chat.type == "private":
        msg.reply_text("🙂 this command is only for groups. You can use hentai/nsfw commands here without enabling hentai")
    elif not is_hentai:
        msg.reply_text("hentai Mode is already Deactivated")
        return ""
    else:
        sql.rem_hentai(chat.id)
        msg.reply_text("Rolled Back to SFW Mode!")
        message = (
            f"<b>{html.escape(chat.title)}:</b>\n"
            f"DEACTIVATED_hentai\n"
            f"<b>Admin:</b> {mention_html(user.id, html.escape(user.first_name))}\n"
        )
        return message


def list_hentai_chats(update: Update, context: CallbackContext):
    chats = sql.get_all_hentai_chats()
    text = "<b>hentai Activated Chats</b>\n"
    for chat in chats:
        try:
            x = context.bot.get_chat(int(*chat))
            name = x.title or x.first_name
            text += f"• <code>{name}</code>\n"
        except (BadRequest, Unauthorized):
            sql.rem_hentai(*chat)
        except RetryAfter as e:
            sleep(e.retry_after)
    update.effective_message.reply_text(text, parse_mode="HTML")



def anal(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_video(hmtai.get("hmtai","anal"))



def ass(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","ass"))


def bdsm(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","bdsm"))


def cum(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","cum"))


def classic(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_video(hmtai.get("hmtai","classic"))


def creampie(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","creampie"))


def xmanga(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","manga"))



def femdom(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","femdom"))



def hentai(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","hentai"))


def incest(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","incest"))


def masturbation(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","masturbation"))


def public(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","public"))


def ero(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","ero"))


def orgy(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","orgy"))


def yuri(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","yuri"))



def pantsu(update, context):
     chat_id = update.effective_chat.id
     if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
     msg = update.effective_message
     msg.reply_photo(hmtai.get("hmtai","pantsu"))


def glasses(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","glasses"))



def cuckold(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","cuckold"))



def blowjob(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","blowjob"))


def boobjob(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","boobjob"))


def footjob(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","footjob"))


def handjob(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_video(hmtai.get("hmtai","handjob"))


def boobs(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","boobs"))


def thigs(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","thigs"))


def pussy(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","pussy"))


def ahegao(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","ahegao"))


def uniform(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","uniform"))


def gangbang(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","gangbang"))




def gifx(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_video(hmtai.get("hmtai","gif"))



def zettai(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("hmtai","zettaiRyouiki"))


def paizuri(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    target = "hentai"
    msg.reply_photo(hmtai.get("nekobot","paizuri"))


def hass(update, context):
    chat_id = update.effective_chat.id
    if update.effective_message.chat.type != "private":
        is_hentai = sql.is_hentai(chat_id)
        if not is_hentai:
            return
    msg = update.effective_message
    msg.reply_photo(hmtai.get("nekobot","hass"))



def waifu(update, context):
    msg = update.effective_message
    target = "waifu"
    with open("temp.png", "wb") as f:
        f.write(requests.get(hmtai.get("nekos","waifu")).content)
    img = Image.open("temp.png")
    img.save("temp.webp", "webp")
    msg.reply_document(open("temp.webp", "rb"))
    os.remove("temp.webp")
    os.remove("temp.png")



def kiss(update, context):
    msg = update.effective_message
    target = "kiss"
    msg.reply_video(hmtai.get("nekos","kiss"))





def hug(update, context):
    msg = update.effective_message
    target = "cuddle"
    msg.reply_video(hmtai.get("nekos","hug"))



def smug(update, context):
    msg = update.effective_message
    msg.reply_video(hmtai.get("nekos","smug"))

def feed(update, context):
    msg = update.effective_message
    msg.reply_video(hmtai.get("nekos","feed"))


ADD_hentai_HANDLER = CommandHandler("addhentai", add_hentai, run_async=True)
REMOVE_hentai_HANDLER = CommandHandler("rmhentai", rem_hentai, run_async=True)
LIST_hentai_CHATS_HANDLER = CommandHandler(
    "hentaichats", list_hentai_chats, filters=CustomFilters.dev_filter, run_async=True)
ANAL_HANDLER = CommandHandler("anal", anal, run_async=True)
ASS_HANDLER = CommandHandler("ass", ass, run_async=True)
BDSM_HANDLER = CommandHandler("bdsm", bdsm, run_async=True)
CUM_HANDLER = CommandHandler("cum", cum, run_async=True)
CLASSIC_HANDLER = CommandHandler("classic", classic, run_async=True)
CREAMPIE_HANDLER = CommandHandler("creampie", creampie, run_async=True)
XMANGA_HANDLER = CommandHandler("xmanga", xmanga, run_async=True)
FEMDOM_HANDLER = CommandHandler("femdom", femdom, run_async=True)
HENTAI_HANDLER = CommandHandler("hentai", hentai, run_async=True)
INCEST_HANDLER = CommandHandler("incest", incest, run_async=True)
MASTURBATION_HANDLER = CommandHandler("masturbation", masturbation, run_async=True)
PUBLIC_HANDLER = CommandHandler("public", public, run_async=True)
ERO_HANDLER = CommandHandler("ero", ero, run_async=True)
ORGY_HANDLER = CommandHandler("orgy", orgy, run_async=True)
YURI_HANDLER = CommandHandler("yuri", yuri, run_async=True)
PANTSU_HANDLER = CommandHandler("pantsu", pantsu, run_async=True)
GLASSES_HANDLER = CommandHandler("glasses", glasses, run_async=True)
CUCKOLD_HANDLER = CommandHandler("cuckold", cuckold, run_async=True)
BLOWJOB_HANDLER = CommandHandler("blowjob", blowjob, run_async=True)
BOOBJOB_HANDLER = CommandHandler("boobjob", boobjob, run_async=True)
FOOTJOB_HANDLER = CommandHandler("footjob", footjob, run_async=True)
HANDJOB_HANDLER = CommandHandler("handjob", handjob, run_async=True)
BOOBS_HANDLER = CommandHandler("boobs", boobs, run_async=True)
THIGS_HANDLER = CommandHandler("thigs", thigs, run_async=True)
PUSSY_HANDLER = CommandHandler("pussy", pussy, run_async=True)
AHEGAO_HANDLER = CommandHandler("ahegao", ahegao, run_async=True)
UNIFORM_HANDLER = CommandHandler("uniform", uniform, run_async=True)
GANGBANG_HANDLER = CommandHandler("gangbang", gangbang, run_async=True)
GIFX_HANDLER = CommandHandler("gifx", gifx, run_async=True)
ZETTAI_HANDLER = CommandHandler("zettai", zettai, run_async=True)
PAIZURI_HANDLER = CommandHandler("paizuri", paizuri, run_async=True)
HASS_HANDLER = CommandHandler("hass", hass, run_async=True)
WAIFU_HANDLER = CommandHandler("waifu", waifu, run_async=True)
KISS_HANDLER = CommandHandler("kiss", kiss, run_async=True)
HUG_HANDLER = CommandHandler("hug", hug, run_async=True)
SMUG_HANDLER = CommandHandler("smug", smug, run_async=True)
FEED_HANDLER = CommandHandler("feed", feed, run_async=True)


dispatcher.add_handler(ADD_hentai_HANDLER)
dispatcher.add_handler(REMOVE_hentai_HANDLER)
dispatcher.add_handler(LIST_hentai_CHATS_HANDLER)
dispatcher.add_handler(ANAL_HANDLER)
dispatcher.add_handler(ASS_HANDLER)
dispatcher.add_handler(BDSM_HANDLER)
dispatcher.add_handler(CUM_HANDLER)
dispatcher.add_handler(CLASSIC_HANDLER)
dispatcher.add_handler(CREAMPIE_HANDLER)
dispatcher.add_handler(XMANGA_HANDLER)
dispatcher.add_handler(FEMDOM_HANDLER)
dispatcher.add_handler(HENTAI_HANDLER)
dispatcher.add_handler(INCEST_HANDLER)
dispatcher.add_handler(MASTURBATION_HANDLER)
dispatcher.add_handler(PUBLIC_HANDLER)
dispatcher.add_handler(ERO_HANDLER)
dispatcher.add_handler(ORGY_HANDLER)
dispatcher.add_handler(YURI_HANDLER)
dispatcher.add_handler(PANTSU_HANDLER)
dispatcher.add_handler(GLASSES_HANDLER)
dispatcher.add_handler(CUCKOLD_HANDLER)
dispatcher.add_handler(BLOWJOB_HANDLER)
dispatcher.add_handler(BOOBJOB_HANDLER)
dispatcher.add_handler(FOOTJOB_HANDLER)
dispatcher.add_handler(HANDJOB_HANDLER)
dispatcher.add_handler(BOOBS_HANDLER)
dispatcher.add_handler(THIGS_HANDLER)
dispatcher.add_handler(PUSSY_HANDLER)
dispatcher.add_handler(AHEGAO_HANDLER)
dispatcher.add_handler(UNIFORM_HANDLER)
dispatcher.add_handler(GANGBANG_HANDLER)
dispatcher.add_handler(GIFX_HANDLER)
dispatcher.add_handler(ZETTAI_HANDLER)
dispatcher.add_handler(PAIZURI_HANDLER)
dispatcher.add_handler(HASS_HANDLER)
dispatcher.add_handler(WAIFU_HANDLER)
dispatcher.add_handler(KISS_HANDLER)
dispatcher.add_handler(HUG_HANDLER)
dispatcher.add_handler(SMUG_HANDLER)
dispatcher.add_handler(FEED_HANDLER)

__handlers__ = [
    ADD_hentai_HANDLER,
    REMOVE_hentai_HANDLER,
    LIST_hentai_CHATS_HANDLER,
    ANAL_HANDLER,
    ASS_HANDLER,
    BDSM_HANDLER,
    CUM_HANDLER,
    CLASSIC_HANDLER,
    CREAMPIE_HANDLER,
    XMANGA_HANDLER,
    FEMDOM_HANDLER,
    HENTAI_HANDLER,
    INCEST_HANDLER,
    MASTURBATION_HANDLER,
    PUBLIC_HANDLER,
    ERO_HANDLER,
    ORGY_HANDLER,
    YURI_HANDLER,
    PANTSU_HANDLER,
    GLASSES_HANDLER,
    CUCKOLD_HANDLER,
    BLOWJOB_HANDLER,
    BOOBJOB_HANDLER,
    FOOTJOB_HANDLER,
    HANDJOB_HANDLER,
    BOOBS_HANDLER,
    THIGS_HANDLER,
    PUSSY_HANDLER,
    AHEGAO_HANDLER,
    UNIFORM_HANDLER,
    GANGBANG_HANDLER,
    GIFX_HANDLER,
    ZETTAI_HANDLER,
    PAIZURI_HANDLER,
    HASS_HANDLER,
    WAIFU_HANDLER,
    KISS_HANDLER,
    HUG_HANDLER,
    SMUG_HANDLER,
    FEED_HANDLER,
]

__help__ = """
ussage:
    
/addhentai : Enable hentai mode on a group.
/rmhentai : Disable hentai mode on a group.
 
Commands :   
**SFW** -

/hug - send random hug gifs.
/waifu - send random waifu stickers via AI.
/smug - send ramdom anime smug gifs.
/kiss - send ramdom kiss gifs.
/feed - send ramdom feed gifs.


**NSFW** -
/anal - 
/ass -
/bdsm -
/cum -
/classic -
/creampie -
/xmanga -
/femdom -
/hentai -
/incest -
/masturbation -
/public -
/ero -
/orgy -
/yuri -
/pantsu -
/glasses -
/cuckold -
/blowjob - 
/footjob -
/handjob -
/boobs -
/thighs -
/pussy -
/ahegao -
/uniform -
/gangbang -
/gifx -
/zettai -
/paizuri -
/hass -


"""

__mod_name__ = "Hentai🔞"
