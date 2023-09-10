import math
from requests import request
from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from telegram import Update
from telegram.ext import CallbackContext, run_async
from telegram.error import BadRequest

RAPID_X_KEY = "673f68d73dmsh715666eacc05574p156574jsn06e2cd81e44d"



def simplify(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return

    lol = message.text.split(" ", 1)

    url = "https://evaluate-expression.p.rapidapi.com/"
    querystring = {"expression": lol[1]}
    headers = {
        "x-rapidapi-key": RAPID_X_KEY,
        "x-rapidapi-host": "evaluate-expression.p.rapidapi.com",
    }
    response = request("GET", url, headers=headers, params=querystring)
    try:
        update.effective_chat.send_message(response.text)
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def cos(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.cos(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def sin(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.sin(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def tan(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.tan(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def arccos(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.acos(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def arcsin(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.asin(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def arctan(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.atan(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def abs(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.fabs(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


def log(update: Update, context: CallbackContext):
    args = context.args
    message = update.effective_message

    if not args:
        update.effective_chat.send_message("What to do with it? see help section of math")
        return
    lol = message.text.split(" ", 1)
    try:
        update.effective_chat.send_message(math.log(int(lol[1])))
    except BadRequest:
        update.effective_chat.send_message("Something went wrong!")
    return


__help__ = """
 • `/math`*:* Math `/math 2^2+2(2)`
 • `/cos`*:* Cosine `/cos pi`
 • `/sin`*:* Sine `/sin 0`
 • `/tan`*:* Tangent `/tan 0`
 • `/arccos`*:* Inverse Cosine `/arccos 1`
 • `/arcsin`*:* Inverse Sine `/arcsin 0`
 • `/arctan`*:* Inverse Tangent `/arctan 0`
 • `/abs`*:* Absolute Value `/abs -1`
 • `/log`*:* Logarithm `/log 2l8`
_Keep in mind_: To find the correct answere supply correct form of requests.
"""

__mod_name__ = "Math"

SIMPLIFY_HANDLER = DisableAbleCommandHandler("math", simplify, run_async=True)
COS_HANDLER = DisableAbleCommandHandler("cos", cos, run_async=True)
SIN_HANDLER = DisableAbleCommandHandler("sin", sin, run_async=True)
TAN_HANDLER = DisableAbleCommandHandler("tan", tan, run_async=True)
ARCCOS_HANDLER = DisableAbleCommandHandler("arccos", arccos, run_async=True)
ARCSIN_HANDLER = DisableAbleCommandHandler("arcsin", arcsin, run_async=True)
ARCTAN_HANDLER = DisableAbleCommandHandler("arctan", arctan, run_async=True)
ABS_HANDLER = DisableAbleCommandHandler("abs", abs, run_async=True)
LOG_HANDLER = DisableAbleCommandHandler("log", log, run_async=True)

dispatcher.add_handler(SIMPLIFY_HANDLER)
dispatcher.add_handler(COS_HANDLER)
dispatcher.add_handler(SIN_HANDLER)
dispatcher.add_handler(TAN_HANDLER)
dispatcher.add_handler(ARCCOS_HANDLER)
dispatcher.add_handler(ARCSIN_HANDLER)
dispatcher.add_handler(ARCTAN_HANDLER)
dispatcher.add_handler(ABS_HANDLER)
dispatcher.add_handler(LOG_HANDLER)

__handlers__ = [
    SIMPLIFY_HANDLER,
    COS_HANDLER,
    SIN_HANDLER,
    TAN_HANDLER,
    ARCCOS_HANDLER,
    ARCSIN_HANDLER,
    ARCTAN_HANDLER,
    ABS_HANDLER,
    LOG_HANDLER,
]

__command_list__ = [
    "math",
    "factor",
    "derive",
    "integrate",
    "zeroes",
    "tangent",
    "area",
    "cos",
    "sin",
    "tan",
    "arccos",
    "arcsin",
    "arctan",
    "abs",
    "log",
]
