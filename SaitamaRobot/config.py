# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open(f'{os.getcwd()}/SaitamaRobot/{config}', 'r') as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 4042547  # integer value, dont use ""
    API_HASH = "26edf5e69b62da2b6c4e3b8336e22f34"
    TOKEN = "6295293651:AAGcIjHlkB3PqXcSlw7qX1uT2S6KAj14oJU"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 6299128233  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "BIackHatDev"
    SUPPORT_CHAT = 'BHatsGroup'  # Your own group for support, do not add the @
    JOIN_LOGGER = -1002058050288  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = -1002058050288  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    ERROR_LOGS = 6299128233  # gives alerts about errors u can kepp same as support chat or even OWNER_ID(bot will give errors personally).

    # RECOMMENDED
    DATABASE_URL = 'postgresql://lucyhrkm:l54ss7__gNQCDpWWmsFi30wNc2jg5zex@tyke.db.elephantsql.com/lucyhrkm'  # needed for any database modules
    LOAD = []
    NO_LOAD = ['cleaner', 'connection', 'tts']
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # OPTIONAL
    # List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = [     

    ]
    # List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = [
        6299128233,
        5751548638,
        5743243857,
        5821581983,

    ]
    # List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = [

    ]
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = [

    ]
    WOLVES = [

    ]
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 8000
    REDIS_URL = 'redis://default:neko69@redis-18084.c289.us-west-1-2.ec2.cloud.redislabs.com:18084/Neko-Free-db'
    MONGO_DB_URI = 'mongodb+srv://BlackHatDev:BlackHatDev@blackhatdev.zk92igo.mongodb.net/?retryWrites=true&w=majority'
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    STRICT_GMUTE = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = 'CAACAgUAAxkBAAENtlVjqy1BwrWHpGccjQnhB5eKsn1z_wAC9AgAAs3AWVUFx9r02wLwGiwE'  # banhammer makima sticker id, the bot will send this sticker before banning or kicking a user in chat.
    TEST_STICKER = ''  # Test Sticker
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = '3OSIXMABP4OEWO65'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'Z88KT2UGX31O'  # Get your API key from https://timezonedb.com/api  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    GENIUS = ''
    REM_BG_API_KEY = 'R9Je1GEfhiwjq8X4uswJve3U'
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    TEMP_DOWNLOAD_DIRECTORY = './'
    ARQ_API_KEY = "PDQVNR-HVFFFP-ZGVHUS-ZHWPFH-ARQ"
    ARQ_API_URL = "https://arq.hamker.dev"
    BOT_ID = 6295293651
    BOT_USERNAME = "@asimpletelegrambot"
    ANI_DB = None
    CHAT_DB = None
    ALLOW_CHATS = True
    DOWN_PATH = "anibot/downloads/"
    KUKI_TOKEN = "ce95970e-8ff5-4ddf-9710-e5fbd54a78f5"


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
