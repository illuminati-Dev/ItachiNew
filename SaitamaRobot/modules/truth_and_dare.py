import html
import random
import requests as r
import urllib.request
from SaitamaRobot import dispatcher
from telegram import ParseMode, Update, Bot
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram.ext import CallbackContext, run_async

def truth(update: Update, context: CallbackContext):
    args = context.args
    x = r.get("https://api.truthordarebot.xyz/v1/truth").json()
    ques = x.get('question')
    update.effective_message.reply_text(ques)

def dare(update: Update, context: CallbackContext):
    args = context.args
    x = r.get("https://api.truthordarebot.xyz/v1/dare").json()
    ques = x.get('question')
    update.effective_message.reply_text(ques)

__help__ = """

❖/dare*:* Get a dare that you will have to do now.

❖/truth*:* Get a question that you will have to tell truth about.

"""

__mod_name__ = "Truth And Dare🎰"
TRUTH_HANDLER = DisableAbleCommandHandler("truth", truth, run_async=True)
DARE_HANDLER = DisableAbleCommandHandler("dare", dare, run_async=True)

dispatcher.add_handler(TRUTH_HANDLER)
dispatcher.add_handler(DARE_HANDLER)
