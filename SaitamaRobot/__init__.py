import logging
import os
import sys
import time
from os import cpu_count
from redis import StrictRedis
from pyrogram import Client, errors
from pytz import timezone
from aiohttp import ClientSession
import telegram.ext as tg
from telethon import TelegramClient
from Python_ARQ import ARQ
from telegraph import Telegraph
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
#from SaitamaRobot.services.quoteapi import Quotly

StartTime = time.time()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.FileHandler('log.txt'),
              logging.StreamHandler()],
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

# if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 6:
    LOGGER.error(
        "You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting."
    )
    sys.exit(1)

ENV = bool(os.environ.get('ENV', False))

if ENV:
    TOKEN = os.environ.get('TOKEN', None)

    try:
        OWNER_ID = int(os.environ.get('OWNER_ID', None))
    except ValueError:
        raise Exception("Your OWNER_ID env variable is not a valid integer.")

    JOIN_LOGGER = os.environ.get('JOIN_LOGGER', None)
    OWNER_USERNAME = os.environ.get("OWNER_USERNAME", None)

    try:
        DRAGONS = {int(x) for x in os.environ.get("DRAGONS", "").split()}
        DEV_USERS = {int(x) for x in os.environ.get("DEV_USERS", "").split()}
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in os.environ.get("DEMONS", "").split()}
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in os.environ.get("WOLVES", "").split()}
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in os.environ.get("TIGERS", "").split()}
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    INFOPIC = bool(os.environ.get('INFOPIC', True))
    EVENT_LOGS = os.environ.get('EVENT_LOGS', None)
    WEBHOOK = bool(os.environ.get('WEBHOOK', False))
    URL = os.environ.get('URL', "")  # Does not contain token
    PORT = int(os.environ.get('PORT', 5000))
    CERT_PATH = os.environ.get("CERT_PATH")
    API_ID = os.environ.get('API_ID', None)
    API_HASH = os.environ.get('API_HASH', None)
    DB_URI = os.environ.get('DATABASE_URL')
    DONATION_LINK = os.environ.get('DONATION_LINK')
    TEMP_DOWNLOAD_DIRECTORY = os.environ.get('./')
    LOAD = os.environ.get("LOAD", "").split()
    NO_LOAD = os.environ.get("NO_LOAD", "translation").split()
    DEL_CMDS = bool(os.environ.get('DEL_CMDS', True))
    STRICT_GBAN = bool(os.environ.get('STRICT_GBAN', True))
    STRICT_GMUTE = bool(os.environ.get('STRICT_GMUTE', True))
    WORKERS = int(os.environ.get('WORKERS', 8))
    BAN_STICKER = os.environ.get('BAN_STICKER',
                                 'CAADAgADOwADPPEcAXkko5EB3YGYAg')
    ARQ_API_KEY = os.environ.get('ARQ_API_KEY')
    ARQ_API_URL = os.environ.get('ARQ_API_URL')
    ALLOW_EXCL = os.environ.get('ALLOW_EXCL', True)
    CASH_API_KEY = os.environ.get('CASH_API_KEY', None)
    TIME_API_KEY = os.environ.get('TIME_API_KEY', None)
    REM_BG_API_KEY = os.environ.get('REM_BG_API_KEY', None)
    GENIUS = os.environ.get('GENIUS', None)
    MONGO_DB_URI = os.environ.get("MONGO_DB_URI", None)
    REDIS_URL = os.environ.get("REDIS_URL", None)
    SUPPORT_CHAT = os.environ.get('SUPPORT_CHAT', None)
    SPAMWATCH_SUPPORT_CHAT = os.environ.get('SPAMWATCH_SUPPORT_CHAT', None)
    SPAMWATCH_API = os.environ.get('SPAMWATCH_API', None)
    BOT_ID = os.environ.get("BOT_ID", None)
    BOT_USERNAME = os.environ.get("BOT_USERNAME", None)
    ALLOW_CHATS = os.environ.get("ALLOW_CHATS", True)
    ANI_DB = os.environ.get('ANI_DB')
    CHAT_DB = os.environ.get('CHAT_DB')
    DOWN_PATH = os.environ.get('DOWN_PATH', 'anibot/downloads/')
    KUKI_TOKEN = os.environ.get('KUKI_TOKEN', None)
    ERROR_LOGS = os.environ.get('ERROR_LOGS', None)

    try:
        BL_CHATS = {int(x) for x in os.environ.get('BL_CHATS', "").split()}
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

else:
    from SaitamaRobot.config import Development as Config

    TOKEN = Config.TOKEN

    try:
        OWNER_ID = int(Config.OWNER_ID)
    except ValueError:
        raise Exception("Your OWNER_ID variable is not a valid integer.")

    JOIN_LOGGER = Config.JOIN_LOGGER
    OWNER_USERNAME = Config.OWNER_USERNAME

    try:
        DRAGONS = {int(x) for x in Config.DRAGONS or []}
        DEV_USERS = {int(x) for x in Config.DEV_USERS or []}
    except ValueError:
        raise Exception(
            "Your sudo or dev users list does not contain valid integers.")

    try:
        DEMONS = {int(x) for x in Config.DEMONS or []}
    except ValueError:
        raise Exception(
            "Your support users list does not contain valid integers.")

    try:
        WOLVES = {int(x) for x in Config.WOLVES or []}
    except ValueError:
        raise Exception(
            "Your whitelisted users list does not contain valid integers.")

    try:
        TIGERS = {int(x) for x in Config.TIGERS or []}
    except ValueError:
        raise Exception(
            "Your tiger users list does not contain valid integers.")

    EVENT_LOGS = Config.EVENT_LOGS
    WEBHOOK = Config.WEBHOOK
    URL = Config.URL
    PORT = Config.PORT
    CERT_PATH = Config.CERT_PATH
    API_ID = Config.API_ID
    API_HASH = Config.API_HASH
    TEMP_DOWNLOAD_DIRECTORY = Config.TEMP_DOWNLOAD_DIRECTORY
    BOT_ID = Config.BOT_ID
    BOT_USERNAME = Config.BOT_USERNAME
    JOIN_LOGGER = Config.JOIN_LOGGER

    DB_URI = Config.DATABASE_URL
    DONATION_LINK = Config.DONATION_LINK
    LOAD = Config.LOAD
    NO_LOAD = Config.NO_LOAD
    DEL_CMDS = Config.DEL_CMDS
    STRICT_GBAN = Config.STRICT_GBAN
    STRICT_GMUTE = Config.STRICT_GMUTE
    WORKERS = Config.WORKERS
    REDIS_URL = Config.REDIS_URL
    MONGO_DB_URI = Config.MONGO_DB_URI
    ARQ_API_KEY = Config.ARQ_API_KEY
    ARQ_API_URL = Config.ARQ_API_URL
    BAN_STICKER = Config.BAN_STICKER
    ALLOW_EXCL = Config.ALLOW_EXCL
    CASH_API_KEY = Config.CASH_API_KEY
    TIME_API_KEY = Config.TIME_API_KEY
    GENIUS = Config.GENIUS
    REM_BG_API_KEY = Config.REM_BG_API_KEY
  #  WALL_API = Config.WALL_API
    SUPPORT_CHAT = Config.SUPPORT_CHAT
    SPAMWATCH_SUPPORT_CHAT = Config.SPAMWATCH_SUPPORT_CHAT
    SPAMWATCH_API = Config.SPAMWATCH_API
    INFOPIC = Config.INFOPIC
    DOWN_PATH = Config.DOWN_PATH
    ANI_DB = Config.ANI_DB
    CHAT_DB = Config.CHAT_DB
    KUKI_TOKEN = Config.KUKI_TOKEN
    ERROR_LOGS = Config.ERROR_LOGS
    ALLOW_CHATS = Config.ALLOW_CHATS

    try:
        BL_CHATS = {int(x) for x in Config.BL_CHATS or []}
    except ValueError:
        raise Exception(
            "Your blacklisted chats list does not contain valid integers.")

DRAGONS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

REDIS = StrictRedis.from_url(REDIS_URL, decode_responses=True)

try:

    REDIS.ping()

    LOGGER.info("Your redis server is now alive!")

except BaseException:

    raise Exception("Your redis server is not alive, please check again.")

finally:

    REDIS.ping()

    LOGGER.info("Your redis server is now alive!")

telegraph = Telegraph()

LOGGER.info("Telegraph installing.")

telegraph.create_account(short_name='Makima')

LOGGER.info("telegraph account creating.")

updater = tg.Updater(
    TOKEN,
    workers=min(32, os.cpu_count() + 4),
    request_kwargs={"read_timeout": 10, "connect_timeout": 10},
)
telethn = TelegramClient("makima", API_ID, API_HASH).start(bot_token=TOKEN)
pbot = Client("makimaPYRO", api_id=API_ID, api_hash=API_HASH, bot_token=TOKEN)
mongo_client = MongoClient(MONGO_DB_URI)
db = mongo_client.SaitamaRobot
dispatcher = updater.dispatcher
aiohttpsession = ClientSession()
arq = ARQ(ARQ_API_URL, ARQ_API_KEY, aiohttpsession)

DRAGONS = list(DRAGONS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WOLVES = list(WOLVES)
DEMONS = list(DEMONS)
TIGERS = list(TIGERS)

# Load at end to ensure all prev variables have been set
from SaitamaRobot.modules.helper_funcs.handlers import (
    CustomCommandHandler,
    CustomMessageHandler,
    CustomRegexHandler,
)
# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler


# -------Quote-------
#quotly = Quotly()
# -------------------
