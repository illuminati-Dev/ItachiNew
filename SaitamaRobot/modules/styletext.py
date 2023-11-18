from SaitamaRobot import dispatcher
from SaitamaRobot.modules.disable import DisableAbleCommandHandler
from SaitamaRobot.modules.helper_funcs.alternate import typing_action
from telegram import ParseMode
from telegram.ext import run_async

normiefont = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z",
]
weebyfont = [
    "卂", "乃", "匚", "刀", "乇", "下", "厶", "卄", "工", "丁", "长", "乚", "从", "𠘨", "口", "尸", "㔿", "尺", "丂", "丅", "凵", "リ", "山", "乂", "丫", "乙",
]
bubblefont = [
    "ⓐ", "ⓑ", "ⓒ", "ⓓ", "ⓔ", "ⓕ", "ⓖ", "ⓗ", "ⓘ", "ⓙ", "ⓚ", "ⓛ", "ⓜ", "ⓝ", "ⓞ", "ⓟ", "ⓠ", "ⓡ", "ⓢ", "ⓣ", "ⓤ", "ⓥ", "ⓦ", "ⓧ", "ⓨ", "ⓩ",
]
fbubblefont = [
    "🅐", "🅑", "🅒", "🅓", "🅔", "🅕", "🅖", "🅗", "🅘", "🅙", "🅚", "🅛", "🅜", "🅝", "🅞", "🅟", "🅠", "🅡", "🅢", "🅣", "🅤", "🅥", "🅦", "🅧", "🅨", "🅩",
]
squarefont = [
    "🄰", "🄱", "🄲", "🄳", "🄴", "🄵", "🄶", "🄷", "🄸", "🄹", "🄺", "🄻", "🄼", "🄽", "🄾", "🄿", "🅀", "🅁", "🅂", "🅃", "🅄", "🅅", "🅆", "🅇", "🅈", "🅉",
]
fsquarefont = [
    "🅰", "🅱", "🅲", "🅳", "🅴", "🅵", "🅶", "🅷", "🅸", "🅹", "🅺", "🅻", "🅼", "🅽", "🅾", "🅿", "🆀", "🆁", "🆂", "🆃", "🆄", "🆅", "🆆", "🆇", "🆈", "🆉",
]
bluefont = [
    "🇦 ", "🇧 ", "🇨 ", "🇩 ", "🇪 ", "🇫 ", "🇬 ", "🇭 ", "🇮 ", "🇯 ", "🇰 ", "🇱 ", "🇲 ", "🇳 ", "🇴 ", "🇵 ", "🇶 ", "🇷 ", "🇸 ", "🇹 ", "🇺 ", "🇻 ", "🇼 ", "🇽 ", "🇾 ", "🇿 ",
]
latinfont = [
    "𝒶", "𝒷", "𝒸", "𝒹", "ℯ", "𝒻", "ℊ", "𝒽", "𝒾", "𝒿", "𝓀", "𝓁", "𝓂", "𝓃", "ℴ", "𝓅", "𝓆", "𝓇", "𝓈", "𝓉", "𝓊", "𝓋", "𝓌", "𝓍", "𝓎", "𝓏",
]
linedfont = [
    "𝕒", "𝕓", "𝕔", "𝕕", "𝕖", "𝕗", "𝕘", "𝕙", "𝕚", "𝕛", "𝕜", "𝕝", "𝕞", "𝕟", "𝕠", "𝕡", "𝕢", "𝕣", "𝕤", "𝕥", "𝕦", "𝕧", "𝕨", "𝕩", "𝕪", "𝕫",
]

def upgrade_text(update, context, font):
    args = context.args
    message = update.effective_message
    string = ""

    if message.reply_to_message:
        string = message.reply_to_message.text.lower().replace(" ", "  ")

    if args:
        string = "  ".join(args).lower()

    if not string:
        message.reply_text(f"Usage is `/{font} <text>`", parse_mode=ParseMode.MARKDOWN)
        return

    for normiecharacter in string:
        if normiecharacter in normiefont:
            font_character = font[normiefont.index(normiecharacter)]
            string = string.replace(normiecharacter, font_character)

    if message.reply_to_message:
        message.reply_to_message.reply_text(string)
    else:
        message.reply_text(string)

@typing_action
def weebify(update, context):
    upgrade_text(update, context, weebyfont)

@typing_action
def bubble(update, context):
    upgrade_text(update, context, bubblefont)

@typing_action
def fbubble(update, context):
    upgrade_text(update, context, fbubblefont)

@typing_action
def square(update, context):
    upgrade_text(update, context, squarefont)

@typing_action
def fsquare(update, context):
    upgrade_text(update, context, fsquarefont)

@typing_action
def blue(update, context):
    upgrade_text(update, context, bluefont)

@typing_action
def latin(update, context):
    upgrade_text(update, context, latinfont)

@typing_action
def lined(update, context):
    upgrade_text(update, context, linedfont)

__help__ = """
 - /weebify <text>: weebify your text!
 - /bubble <text>: bubble your text!
 - /fbubble <text>: bubble-filled your text!
 - /square <text>: square your text!
 - /fsquare <text>: square-filled your text!
 - /blue <text>: bluify your text!
 - /latin <text>: latinify your text!
 - /lined <text>: lined your text!
"""
__mod_name__ = "StyleText💫"

WEEBIFY_HANDLER = DisableAbleCommandHandler("weebify", weebify, run_async=True)
BUBBLE_HANDLER = DisableAbleCommandHandler("bubble", bubble, run_async=True)
FBUBBLE_HANDLER = DisableAbleCommandHandler("fbubble", fbubble, run_async=True)
SQUARE_HANDLER = DisableAbleCommandHandler("square", square, run_async=True)
FSQUARE_HANDLER = DisableAbleCommandHandler("fsquare", fsquare, run_async=True)
BLUE_HANDLER = DisableAbleCommandHandler("blue", blue, run_async=True)
LATIN_HANDLER = DisableAbleCommandHandler("latin", latin, run_async=True)
LINED_HANDLER = DisableAbleCommandHandler("lined", lined, run_async=True)

dispatcher.add_handler(WEEBIFY_HANDLER)
dispatcher.add_handler(BUBBLE_HANDLER)
dispatcher.add_handler(FBUBBLE_HANDLER)
dispatcher.add_handler(SQUARE_HANDLER)
dispatcher.add_handler(FSQUARE_HANDLER)
dispatcher.add_handler(BLUE_HANDLER)
dispatcher.add_handler(LATIN_HANDLER)
dispatcher.add_handler(LINED_HANDLER)

__command_list__ = ["weebify", "bubble", "fbubble", "square", "fsquare", "blue", "latin", "lined"]
__handlers__ = [WEEBIFY_HANDLER, BUBBLE_HANDLER, FBUBBLE_HANDLER, SQUARE_HANDLER, FSQUARE_HANDLER, BLUE_HANDLER, LATIN_HANDLER, LINED_HANDLER]
