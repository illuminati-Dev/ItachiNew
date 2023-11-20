import importlib
import time
import re
from sys import argv
from typing import Optional

from SaitamaRobot import (ALLOW_EXCL, CERT_PATH, DONATION_LINK, LOGGER,
                          OWNER_ID, PORT, SUPPORT_CHAT, TOKEN, URL, WEBHOOK,
                          dispatcher, StartTime, telethn, updater, pbot)
# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from SaitamaRobot.modules import ALL_MODULES
from SaitamaRobot.modules.helper_funcs.chat_status import is_user_admin
from SaitamaRobot.modules.helper_funcs.misc import paginate_modules
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup, ParseMode,
                      Update)
from telegram.error import (BadRequest, ChatMigrated, NetworkError,
                            TelegramError, TimedOut, Unauthorized)
from telegram.ext import (CallbackContext, CallbackQueryHandler, CommandHandler,
                          Filters, MessageHandler)
from telegram.ext.dispatcher import DispatcherHandlerStop, run_async
from telegram.utils.helpers import escape_markdown

TEST = -1002058050288

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += f"{time_list.pop()}, "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time


PM_START_TEXT = """
────「 [Itachi Uchiha](https://graph.org/file/863d9e30f84f9168f5c28.jpg) 」────
Hola! {},
My Name Is {}◎! ㅤ
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
◍ I Am  a Group Management Bot , Built For Weebs.
➖➖➖➖➖➖➖➖➖➖➖➖➖➖
◍ I Am Specialized In Managing Groups Of Anime Communities⚝!
"""

buttons = [
    [
        InlineKeyboardButton(
            text="➕️ 𝘼𝙙𝙙 𝙄𝙩𝙖𝙘𝙝𝙞 𝙏𝙤 𝙈𝙖𝙣𝙖𝙜𝙚 𝙔𝙤𝙪𝙧 𝙂𝙧𝙤𝙪𝙥 ➕️",
            url="t.me/Itachi_UchihaXBot?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(
            text="🛠𝙐𝙥𝙙𝙖𝙩𝙚𝙨 𝘾𝙝𝙖𝙣𝙣𝙚𝙡", url="https://t.me/UchihaPoliceUpdate"
        ),
        InlineKeyboardButton(
            text="💬𝙎𝙪𝙥𝙥𝙤𝙧𝙩 𝙂𝙧𝙤𝙪𝙥", url=f"https://t.me/{SUPPORT_CHAT}"
        ),
    ],
    [
        InlineKeyboardButton(text="👁️‍🗨️𝘿𝙚𝙫𝙚𝙡𝙤𝙥𝙚𝙧", url="https://t.me/BIackHatDev"),
        InlineKeyboardButton(
            text="🌐𝙊𝙪𝙧 𝙉𝙚𝙩𝙬𝙤𝙧𝙠", url="https://t.me/Emperors_Network"
        ),
    ],
    [
        InlineKeyboardButton(
            text="💡𝙃𝙚𝙡𝙥 𝙖𝙣𝙙 𝘾𝙤𝙢𝙢𝙖𝙣𝙙𝙨", callback_data="help_back"
        ),
    ],
]

HELP_STRINGS = """
ʜᴇʏ ᴛʜᴇʀᴇ! ᴍʏ ɴᴀᴍᴇ ɪs *{}*.
ɪ'ᴍ ᴀ ᴘᴀʀᴛ ᴏғ [TheKaizers](https://t.me/UchihaPolice_Support)
ʜᴀᴠᴇ ᴀ ʟᴏᴏᴋ ᴀᴛ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ ғᴏʀ ᴀɴ ɪᴅᴇᴀ ᴏғ sᴏᴍᴇ ᴏғ ᴛʜᴇ ᴛʜɪɴɢs ɪ ᴄᴀɴ ʜᴇʟᴘ ʏᴏᴜ ᴡɪᴛʜ.

*ᴍᴀɪɴ* ᴄᴏᴍᴍᴀɴᴅs ᴀᴠᴀɪʟᴀʙʟᴇ: 
 • /help: ᴘᴍ's ʏᴏᴜ ᴛʜɪs ᴍᴇssᴀɢᴇ. 
 • /help <ᴍᴏᴅᴜʟᴇ ɴᴀᴍᴇ>: ᴘᴍ's ʏᴏᴜ ɪɴғᴏ ᴀʙᴏᴜᴛ ᴛʜᴀᴛ ᴍᴏᴅᴜʟᴇ. 
 • /donate: ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴏɴ ʜᴏᴡ ᴛᴏ ᴅᴏɴᴀᴛᴇ! 
 • /settings:  
 • ɪɴ ᴘᴍ: ᴡɪʟʟ sᴇɴᴅ ʏᴏᴜ ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ғᴏʀ ᴀʟʟ sᴜᴘᴘᴏʀᴛᴇᴅ ᴍᴏᴅᴜʟᴇs. 
 • ɪɴ ᴀ ɢʀᴏᴜᴘ: ᴡɪʟʟ ʀᴇᴅɪʀᴇᴄᴛ ʏᴏᴜ ᴛᴏ ᴘᴍ, ᴡɪᴛʜ ᴀʟʟ ᴛʜᴀᴛ ᴄʜᴀᴛ's sᴇᴛᴛɪɴɢs.    
 {}

 ᴀɴᴅ ᴛʜᴇ ғᴏʟʟᴏᴡɪɴɢ:
""".format(
    dispatcher.bot.first_name,
    "•All commands can either be used with / or !.\n" if ALLOW_EXCL else "",
)

# SAITAMA_IMG = "https://graph.org/file/863d9e30f84f9168f5c28.jpg"

DONATE_STRING = """Heya, glad to hear you want to donate!
Saitama is hosted on one of Kaizoku's Servers and doesn't require any donations as of now but \
You can donate to the original writer of the Base code, Paul
There are two ways of supporting him; [PayPal](paypal.me/PaulSonOfLars), or [Monzo](monzo.me/paulnionvestergaardlarsen)."""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("SaitamaRobot.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if imported_module.__mod_name__.lower() not in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception(
            "Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module


# do not async
def send_help(chat_id, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    dispatcher.bot.send_message(
        chat_id=chat_id,
        text=text,
        parse_mode=ParseMode.MARKDOWN,
        disable_web_page_preview=True,
        reply_markup=keyboard)


def start(update: Update, context: CallbackContext):
    args = context.args
    uptime = get_readable_time((time.time() - StartTime))
    if update.effective_chat.type == "private":
        if len(args) >= 1:
            if args[0].lower() == "help":
                send_help(update.effective_chat.id, HELP_STRINGS)
            elif args[0].lower().startswith("ghelp_"):
                mod = args[0].lower().split('_', 1)[1]
                if not HELPABLE.get(mod, False):
                    return
                send_help(
                    update.effective_chat.id, HELPABLE[mod].__help__,
                    InlineKeyboardMarkup([[
                        InlineKeyboardButton(
                            text="Back", callback_data="help_back")
                    ]]))
            elif args[0].lower() == "markdownhelp":
                IMPORTED["extras"].markdown_help_sender(update)
            elif args[0].lower() == "disasters":
                IMPORTED["disasters"].send_disasters(update)
            elif args[0].lower().startswith("stngs_"):
                match = re.match("stngs_(.*)", args[0].lower())
                chat = dispatcher.bot.getChat(match[1])

                if is_user_admin(chat, update.effective_user.id):
                    send_settings(match[1], update.effective_user.id, False)
                else:
                    send_settings(match[1], update.effective_user.id, True)

            elif args[0][1:].isdigit() and "rules" in IMPORTED:
                IMPORTED["rules"].send_rules(update, args[0], from_pm=True)

        else:
            first_name = update.effective_user.first_name
            update.effective_message.reply_text(

                PM_START_TEXT.format(
                    escape_markdown(first_name),
                    escape_markdown(context.bot.first_name)),
                parse_mode=ParseMode.MARKDOWN,

                reply_markup=InlineKeyboardMarkup(buttons),
                timeout=60,

            )

    else:
        update.effective_message.reply_text(
            "I'm online!\n<b>Up since:</b> <code>{}</code>".format(uptime),
            parse_mode=ParseMode.HTML)


# for test purposes
def error_callback(update: Update, context: CallbackContext):
    error = context.error
    try:
        raise error
    except Unauthorized:
        print("no nono1")
        print(error)
        # remove update.message.chat_id from conversation list
    except BadRequest:
        print("no nono2")
        print("BadRequest caught")
        print(error)

        # handle malformed requests - read more below!
    except TimedOut:
        print("no nono3")
        # handle slow connection problems
    except NetworkError:
        print("no nono4")
        # handle other connection problems
    except ChatMigrated as err:
        print("no nono5")
        print(err)
        # the chat_id of a group has changed, use e.new_chat_id instead
    except TelegramError:
        print(error)
        # handle all other telegram related errors


def help_button(update, context):
    query = update.callback_query
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)

    print(query.message.chat.id)

    try:
        if mod_match:
            module = mod_match[1]
            text = ("Here is the help for the *{}* module:\n".format(
                HELPABLE[module].__mod_name__) + HELPABLE[module].__help__)
            query.message.edit_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[
                    InlineKeyboardButton(
                        text="Back", callback_data="help_back")
                ]]))

        elif prev_match:
            curr_page = int(prev_match[1])
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(curr_page - 1, HELPABLE, "help")))

        elif next_match:
            next_page = int(next_match[1])
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")))

        elif back_match:
            query.message.edit_text(
                text=HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")))

        # ensure no spinny white circle
        context.bot.answer_callback_query(query.id)
        # query.message.delete()

    except BadRequest:
        pass


def makima_about_callback(update, context):
    query = update.callback_query
    if query.data == "makima_":
        query.message.edit_text(
            text=""" Hi..🤗 I'm *Itachi*
                 \nHere is the [Source Code](https://github.com/) .""",
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text="Go Back", callback_data="makima_back")
                    ]
                ]
            ),
        )
    elif query.data == "makima_back":
        first_name = update.effective_user.first_name
        query.message.edit_text(
            PM_START_TEXT.format(
                escape_markdown(first_name),
                escape_markdown(context.bot.first_name)),
            parse_mode=ParseMode.MARKDOWN,

            reply_markup=InlineKeyboardMarkup(buttons),
            timeout=60,

        )


def get_help(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    args = update.effective_message.text.split(None, 1)

    # ONLY send help in PM
    if chat.type != chat.PRIVATE:
        if len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
            module = args[1].lower()
            update.effective_message.reply_text(
                f"Contact me in PM to get help of {module.capitalize()}",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help",
                                url=f"t.me/{context.bot.username}?start=ghelp_{module}",
                            )
                        ]
                    ]
                ),
            )

            return
        update.effective_message.reply_text(
            "Contact me in PM to get the list of possible commands.",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Help",
                            url=f"t.me/{context.bot.username}?start=help",
                        )
                    ]
                ]
            ),
        )

        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = "Here is the available help for the *{}* module:\n".format(HELPABLE[module].__mod_name__) \
               + HELPABLE[module].__help__
        send_help(
            chat.id, text,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="Back",
                                       callback_data="help_back")]]))

    else:
        send_help(chat.id, HELP_STRINGS)


def send_settings(chat_id, user_id, user=False):
    if user:
        if USER_SETTINGS:
            settings = "\n\n".join("*{}*:\n{}".format(
                mod.__mod_name__, mod.__user_settings__(user_id))
                                   for mod in USER_SETTINGS.values())
            dispatcher.bot.send_message(
                user_id,
                "These are your current settings:" + "\n\n" + settings,
                parse_mode=ParseMode.MARKDOWN)

        else:
            dispatcher.bot.send_message(
                user_id,
                "Seems like there aren't any user specific settings available :'(",
                parse_mode=ParseMode.MARKDOWN)

    elif CHAT_SETTINGS:
        chat_name = dispatcher.bot.getChat(chat_id).title
        dispatcher.bot.send_message(
            user_id,
            text=f"Which module would you like to check {chat_name}'s settings for?",
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
            ),
        )

    else:
        dispatcher.bot.send_message(
            user_id,
            "Seems like there aren't any chat settings available :'(\nSend this "
            "in a group chat you're admin in to find its current settings!",
            parse_mode=ParseMode.MARKDOWN)


def settings_button(update: Update, context: CallbackContext):
    query = update.callback_query
    user = update.effective_user
    bot = context.bot
    mod_match = re.match(r"stngs_module\((.+?),(.+?)\)", query.data)
    prev_match = re.match(r"stngs_prev\((.+?),(.+?)\)", query.data)
    next_match = re.match(r"stngs_next\((.+?),(.+?)\)", query.data)
    back_match = re.match(r"stngs_back\((.+?)\)", query.data)
    try:
        if mod_match:
            chat_id = mod_match[1]
            module = mod_match[2]
            chat = bot.get_chat(chat_id)
            text = "*{}* has the following settings for the *{}* module:\n\n".format(escape_markdown(chat.title),
                                                                                     CHAT_SETTINGS[
                                                                                         module].__mod_name__) + \
                   CHAT_SETTINGS[module].__chat_settings__(chat_id, user.id)
            query.message.reply_text(
                text=text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Back",
                                callback_data=f"stngs_back({chat_id})",
                            )
                        ]
                    ]
                ),
            )


        elif prev_match:
            chat_id = prev_match[1]
            curr_page = int(prev_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                f"Hi there! There are quite a few settings for {chat.title} - go ahead and pick what you're interested in.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        curr_page - 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )


        elif next_match:
            chat_id = next_match[1]
            next_page = int(next_match[2])
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                f"Hi there! There are quite a few settings for {chat.title} - go ahead and pick what you're interested in.",
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(
                        next_page + 1, CHAT_SETTINGS, "stngs", chat=chat_id
                    )
                ),
            )


        elif back_match:
            chat_id = back_match[1]
            chat = bot.get_chat(chat_id)
            query.message.reply_text(
                text=f"Hi there! There are quite a few settings for {escape_markdown(chat.title)} - go ahead and pick what you're interested in.",
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, CHAT_SETTINGS, "stngs", chat=chat_id)
                ),
            )

        # ensure no spinny white circle
        bot.answer_callback_query(query.id)
        query.message.delete()
    except BadRequest as excp:
        if excp.message not in [
            "Message is not modified",
            "Query_id_invalid",
            "Message can't be deleted",
        ]:
            LOGGER.exception("Exception in settings buttons. %s",
                             str(query.data))


def get_settings(update: Update, context: CallbackContext):
    chat = update.effective_chat  # type: Optional[Chat]
    user = update.effective_user  # type: Optional[User]
    msg = update.effective_message  # type: Optional[Message]

    # ONLY send settings in PM
    if chat.type == chat.PRIVATE:
        send_settings(chat.id, user.id, True)

    elif is_user_admin(chat, user.id):
        text = "Click here to get this chat's settings, as well as yours."
        msg.reply_text(
            text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Settings",
                            url=f"t.me/{context.bot.username}?start=stngs_{chat.id}",
                        )
                    ]
                ]
            ),
        )

    else:
        text = "Click here to check your settings."


def donate(update: Update, context: CallbackContext):
    user = update.effective_message.from_user
    chat = update.effective_chat  # type: Optional[Chat]
    bot = context.bot
    if chat.type == "private":
        update.effective_message.reply_text(
            DONATE_STRING,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True)

        if OWNER_ID != 254318997 and DONATION_LINK:
            update.effective_message.reply_text(
                f"You can also donate to the person currently running me [here]({DONATION_LINK})",
                parse_mode=ParseMode.MARKDOWN,
            )


    else:
        try:
            bot.send_message(
                user.id,
                DONATE_STRING,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True)

            update.effective_message.reply_text(
                "I've PM'ed you about donating to my creator!")
        except Unauthorized:
            update.effective_message.reply_text(
                "Contact me in PM first to get donation information.")


def migrate_chats(update: Update, _: CallbackContext):
    msg = update.effective_message  # type: Optional[Message]
    if msg.migrate_to_chat_id:
        old_chat = update.effective_chat.id
        new_chat = msg.migrate_to_chat_id
    elif msg.migrate_from_chat_id:
        old_chat = msg.migrate_from_chat_id
        new_chat = update.effective_chat.id
    else:
        return

    LOGGER.info("Migrating from %s, to %s", str(old_chat), str(new_chat))
    for mod in MIGRATEABLE:
        mod.__migrate__(old_chat, new_chat)

    LOGGER.info("Successfully migrated!")
    raise DispatcherHandlerStop


def main():
    if TEST is not None:
        try:
            dispatcher.bot.sendMessage(TEST,
                                       "[Any technique is worthless before my eyes!](https://telegra.ph/file/989f55a82dc6de16fa01b.mp4)",
                                       parse_mode=ParseMode.MARKDOWN)
        except Unauthorized:
            LOGGER.warning(
                "Bot isn't able to send message to support_chat, go and check!")
        except BadRequest as e:
            LOGGER.warning(e.message)

    start_handler = CommandHandler("start", start, run_async=True)

    help_handler = CommandHandler("help", get_help, run_async=True)
    help_callback_handler = CallbackQueryHandler(
        help_button, pattern=r"help_.*", run_async=True)

    settings_handler = CommandHandler("settings", get_settings, run_async=True)
    settings_callback_handler = CallbackQueryHandler(
        settings_button, pattern=r"stngs_", run_async=True)

    about_callback_handler = CallbackQueryHandler(
        makima_about_callback, pattern=r"makima_", run_async=True)

    donate_handler = CommandHandler("donate", donate, run_async=True)
    migrate_handler = MessageHandler(Filters.status_update.migrate,
                                     migrate_chats)

    # dispatcher.add_handler(test_handler)
    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(about_callback_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(help_callback_handler)
    dispatcher.add_handler(settings_callback_handler)
    dispatcher.add_handler(migrate_handler)
    dispatcher.add_handler(donate_handler)

    dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info(f"{dispatcher.bot.first_name} is now Up, Using Webhooks!")
        updater.start_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=TOKEN,
            drop_pending_updates=False,
            webhook_url=URL + TOKEN,
            allowed_updates=Update.ALL_TYPES,
        )

        if CERT_PATH:
            updater.bot.set_webhook(
                url=URL + TOKEN, certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Itachi Is Now Alive!")
        updater.start_polling(
            timeout=15,
            read_latency=4,
            drop_pending_updates=True,
        )

    if len(argv) in {1, 3, 4}:
        telethn.run_until_disconnected()

    else:
        telethn.disconnect()
    updater.idle()


if __name__ == '__main__':
    LOGGER.info(f"Successfully loaded modules: {str(ALL_MODULES)}")
    telethn.start(bot_token=TOKEN)
    LOGGER.info("Telethon Started.")
   # pbot.start()
    main()
