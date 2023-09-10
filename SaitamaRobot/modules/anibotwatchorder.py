from pyrogram import filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from pyrogram.enums import ParseMode
from SaitamaRobot import BOT_USERNAME as  BOT_NAME, pbot as anibot
from SaitamaRobot.utlis.helper import check_user, control_user
from SaitamaRobot.utlis.db import get_collection
from SaitamaRobot.utlis.data_parser import get_wo, get_wols

DC = get_collection('DISABLED_CMDS')
WATCH_IMG = "https://telegra.ph/file/8dce442ab9116e2642d11.mp4"


@anibot.on_message(filters.command(["watchorder", f"watchorder{BOT_NAME}"]))
@control_user
async def get_watch_order(client: anibot, message: Message, mdata: dict):
    """Get List of Scheduled Anime"""
    gid = mdata['chat']['id']
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'watch' in find_gc['cmd_list'].split():
        return
    x = message.text.split(" ", 1)
    if len(x)==1:
        await message.reply_animation(WATCH_IMG, caption="""Format : /watchorder < anime name >""", parse_mode=ParseMode.MARKDOWN)
        return
    user = mdata['from_user']['id']
    data = get_wols(x[1])
    msg = f"Found related animes for the query {x[1]}"
    if data == []:
        await message.reply_text('No results found!!!')
        return
    buttons = [
        [
            InlineKeyboardButton(
                str(i[1]), callback_data=f"watch_{i[0]}_{x[1]}_0_{user}"
            )
        ]
        for i in data
    ]

    await message.reply_text(msg, reply_markup=InlineKeyboardMarkup(buttons))


@anibot.on_callback_query(filters.regex(pattern=r"watch_(.*)"))
@check_user
async def watch_(client: anibot, cq: CallbackQuery, cdata: dict):
    kek, id_, qry, req, user = cdata['data'].split("_")
    msg, total = get_wo(int(id_), int(req))
    totalpg, lol = divmod(total, 50)
    button = []
    if lol!=0:
        totalpg + 1
    if total>50:
        if int(req)==0:
            button.append([InlineKeyboardButton(text="Next", callback_data=f"{kek}_{id_}_{qry}_{int(req)+1}_{user}")])
        elif int(req)==totalpg:
            button.append([InlineKeyboardButton(text="Prev", callback_data=f"{kek}_{id_}_{qry}_{int(req)-1}_{user}")])
        else:
            button.append(
                [
                    InlineKeyboardButton(text="Prev", callback_data=f"{kek}_{id_}_{qry}_{int(req)-1}_{user}"),
                    InlineKeyboardButton(text="Next", callback_data=f"{kek}_{id_}_{qry}_{int(req)+1}_{user}")
                ]
            )
    button.append([InlineKeyboardButton("Back", callback_data=f"wol_{qry}_{user}")])
    await cq.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(button))


@anibot.on_callback_query(filters.regex(pattern=r"wol_(.*)"))
@check_user
async def wls(client: anibot, cq: CallbackQuery, cdata: dict):
    kek, qry, user = cdata['data'].split("_")
    data = get_wols(qry)
    msg = f"Found related animes for the query {qry}"
    buttons = [
        [
            InlineKeyboardButton(
                str(i[1]), callback_data=f"watch_{i[0]}_{qry}_0_{user}"
            )
        ]
        for i in data
    ]

    await cq.edit_message_text(msg, reply_markup=InlineKeyboardMarkup(buttons))
