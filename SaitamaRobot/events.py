from telethon import events
from telethon.tl import *
from SaitamaRobot import telethn


def register(**args):
    """ Registers a new message. """
    pattern = args.get('pattern', None)

    r_pattern = r'^[/!]'

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    args['pattern'] = pattern.replace('^/', r_pattern, 1)

    def decorator(func):
        telethn.add_event_handler(func, events.NewMessage(**args))
        return func

    return decorator


def chataction(**args):
    """ Registers chat actions. """
    def decorator(func):
        telethn.add_event_handler(func, events.ChatAction(**args))
        return func

    return decorator


def userupdate(**args):
    """ Registers user updates. """
    def decorator(func):
        telethn.add_event_handler(func, events.UserUpdate(**args))
        return func

    return decorator


def inlinequery(**args):
    """ Registers inline query. """
    pattern = args.get('pattern', None)

    if pattern is not None and not pattern.startswith('(?i)'):
        args['pattern'] = '(?i)' + pattern

    def decorator(func):
        telethn.add_event_handler(func, events.InlineQuery(**args))
        return func

    return decorator


def callbackquery(**args):
    """ Registers inline query. """
    def decorator(func):
        telethn.add_event_handler(func, events.CallbackQuery(**args))
        return func

    return decorator

async def check_permissions(event, user_id, p="", cb=False):
    try:
        pp = await event.client(
            functions.channels.GetParticipantRequest(e.chat_id, user_id)
        )
    except:
        return False
    pp = pp.participant
    if isinstance(pp, types.ChannelParticipant):
        if cb:
            await event.answer("You should be admin to-do it!")
        else:
            await event.reply("You should be admin to-do it!")
        return False
    elif isinstance(pp, types.ChannelParticipantCreator):
        return True
    elif isinstance(pp, types.ChannelParticipantAdmin):
        if p == "add_admins":
            if pp.admin_rights.add_admins:
                return True
            if cb:
                await event.answer(
                    "You are missing the following rights to use this command: CanPromoteUsers.",
                    alert=True,
                )
            else:
                await event.reply(
                    "You are missing the following rights to use this command: CanPromoteUsers."
                )
        elif p == "ban_users":
            if pp.admin_rights.ban_users:
                return True
            if cb:
                await event.answer(
                    "You are missing the following rights to use this command: CanRestrictMembers.",
                    alert=True,
                )
            else:
                await event.reply(
                    "You are missing the following rights to use this command: CanRestrictMembers."
                )
        elif p == "change_info":
            if pp.admin_rights.change_info:
                return True
            if cb:
                await event.answer(
                    "You are missing the following rights to use this command: CanChangeInfo.",
                    alert=True,
                )
            else:
                await event.reply(
                    "You are missing the following rights to use this command: CanChangeInfo."
                )
        elif p == "delete_messages":
            if pp.admin_rights.delete_messages:
                return True
            if cb:
                await event.answer(
                    "You are missing the following rights to use this command: CanDeleteMessages.",
                    alert=True,
                )
            else:
                await event.reply(
                    "You are missing the following rights to use this command: CanDeleteMessages."
                )
        return False
