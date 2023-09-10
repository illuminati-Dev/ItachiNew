import requests
from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram import ParseMode, Update
from telegram.error import BadRequest
from telegram.ext import CallbackContext, run_async


def ud(update: Update, context: CallbackContext):
    msg = update.effective_message
    args = context.args
    text = " ".join(args).lower()
    if not text:
        msg.reply_text("Please enter keywords to search on ud!")
        return
    if text == "makima":
        msg.reply_text("Makima is a Chainsaw Man character and a famous bot made with anime theme by @teamwarlords")
        return
    try:
        results = requests.get(f"http://api.urbandictionary.com/v0/define?term={text}").json()
        reply_text = f'Word:{text}\n\n Definition:\n{results["list"][0]["definition"]}'
        reply_text += f'\n\nExample: \n{results["list"][0]["example"]}'
    except IndexError:
        reply_text = (
            f"Word: {text}\n\nResults: Sorry could not find any matching results!"
        )
    ignore_chars = "[]"
    reply = reply_text
    for chars in ignore_chars:
        reply = reply.replace(chars, "")
    if len(reply) >= 4096:
        reply = reply[:4096]  # max msg lenth of tg.
    try:
        msg.reply_text(reply)
    except BadRequest as err:
        msg.reply_text(f"Error! {err.message}")


UD_HANDLER = DisableAbleCommandHandler(["ud"], ud, run_async=True)

dispatcher.add_handler(UD_HANDLER)

__command_list__ = ["ud"]
__handlers__ = [UD_HANDLER]
