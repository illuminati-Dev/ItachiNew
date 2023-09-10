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
    TOKEN = "1979449216:AAEWAmR-m5PkmMLnUJYy3oaD5dABM0n2WbM"  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    OWNER_ID = 1973983574  # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "Wolverineeex"
    SUPPORT_CHAT = 'Makima_Bot_Support'  # Your own group for support, do not add the @
    JOIN_LOGGER = -1001544884219  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = -1001544884219  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit
    ERROR_LOGS = 1476517140  # gives alerts about errors u can kepp same as support chat or even OWNER_ID(bot will give errors personally).

    # RECOMMENDED
    DATABASE_URL = 'postgresql://makima:makima1234@132.145.204.100:5432/makima'  # needed for any database modules
    LOAD = []
    NO_LOAD = ['cleaner', 'connection']
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = "MNo3lF_tu8hYL1sojQi~F5fdMEhKwDwVvPFmx0Fd9B6DovG74fU0U2sBhpRamK2J"  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"

    # OPTIONAL
    # List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = [
        917790252,
        1380685014,
        1172340595,
        1869271514,
        1435293433,
        2107137268,
        1858995207,
        1649093710,
        1719660492,

    ]
    # List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = [
        1476517140,
        1711005257,

    ]
    # List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = [
        5555455171,

    ]
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = [
        1827695840,
        1694138821,

    ]
    WOLVES = [

    ]
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    REDIS_URL = 'redis://Godanuj:Godanuj_123@redis-15994.c12.us-east-1-4.ec2.cloud.redislabs.com:15994/Godanuj'
    MONGO_DB_URI = 'mongodb+srv://makima:makima@cluster0.fid6i.mongodb.net/cluster0?retryWrites=true&w=majority'
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    STRICT_GMUTE = True
    WORKERS = 8  # Number of subthreads to use. Set as number of threads your processor uses
    BAN_STICKER = 'CAACAgUAAxkBAAENtlVjqy1BwrWHpGccjQnhB5eKsn1z_wAC9AgAAs3AWVUFx9r02wLwGiwE'  # banhammer makima sticker id, the bot will send this sticker before banning or kicking a user in chat.
    TEST_STICKER = ''  # Test Sticker
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = '3OSIXMABP4OEWO65'  # Get your API key from https://www.alphavantage.co/support/#api-key
    TIME_API_KEY = 'Z88KT2UGX31O'  # Get your API key from https://timezonedb.com/api  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    GENIUS = '4wOHQcDEh5gM_XzGU9moT4r--IWyiqVogo1V3SLNcn0q2G8ksjzKR0JJDa8lTHcA'
    REM_BG_API_KEY = 'R9Je1GEfhiwjq8X4uswJve3U'
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    TEMP_DOWNLOAD_DIRECTORY = './'
    ARQ_API_KEY = "PDQVNR-HVFFFP-ZGVHUS-ZHWPFH-ARQ"
    ARQ_API_URL = "https://arq.hamker.dev"
    BOT_ID = 1979449216
    BOT_USERNAME = "@makima_ultraxbot"
    ANI_DB = "mongodb+srv://userbot:userbot@cluster0.ltasu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    CHAT_DB = "mongodb+srv://userbot:userbot@cluster0.ltasu.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
    ALLOW_CHATS = True
    DOWN_PATH = "anibot/downloads/"
    KUKI_TOKEN = "ce95970e-8ff5-4ddf-9710-e5fbd54a78f5"


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
