import re
from datetime import timedelta

import telethon

from userbot import is_mongo_alive, bot, BOTLOG_CHATID, CMD_HELP, LOGS
from userbot.decorators import register
from userbot.modules.dbhelper import add_filter, get_listeners, delete_listener, get_all_listeners


@register(incoming=True, disable_errors=True)
async def filter_incoming_handler(handler: telethon.events.newmessage.NewMessage):
    """ Checks if the incoming message contains handler of a filter """
    try:
        sender = await handler.get_sender()
        if not hasattr(sender, 'bot') or not sender.bot:
            if not is_mongo_alive():
                await bot.send_message(BOTLOG_CHATID, "`Database connections failing!`")
                return

            listeners = await get_listeners(str(handler.chat_id))
            if not listeners:
                return
            for trigger in listeners:
                pattern = r"( |^|[^\w])" + re.escape(
                    trigger["keyword"]) + r"( |$|[^\w])"
                if re.search(pattern, handler.text, flags=re.IGNORECASE):
                    chat_from = handler.chat if handler.chat else (
                        await handler.get_chat())  # telegram MAY not send the chat enity
                    chat_title = chat_from.title if hasattr(chat_from, 'title') else handler.chat_id
                    if hasattr(chat_from, 'megagroup'):
                        await bot.send_message(BOTLOG_CHATID, silent=False, schedule=timedelta(minutes=1),
                                               message=(f"`{trigger['keyword']}` **HIT**\n\n"
                                                        f"[{chat_title}](https://t.me/{chat_title}/{handler.id})\n"
                                                        f"{handler.text}"))
                    else:
                        await bot.send_message(BOTLOG_CHATID, silent=False, schedule=timedelta(minutes=1),
                                               message=(f"`{trigger['keyword']}` **HIT**\n\n"
                                                        f"**From**: [@{sender.first_name}](tg://user?id={sender.id})\n"
                                                        f"**Text**: {handler.text}")
                                               )
                    return
    except AttributeError as err:
        LOGS.exception(f'{handler.chat_id} - {err}')


@register(outgoing=True, pattern="^.listen(?: |$)(-?\\d+) (\\w+)")
async def add_new_listener(event):
    """ Command for adding a new filter """
    if not is_mongo_alive():
        await event.edit("`Database connections failing!`")
        return

    chat_id = event.pattern_match.group(1)
    keyword = event.pattern_match.group(2)
    if not chat_id or not chat_id:
        await event.edit("`You have to specify a chatid and a keyword!`")
        return

    msg = f"`Listen to `**{keyword}**` on chat `**{chat_id}**"

    if await add_filter(chat_id, keyword) is True:
        await event.edit(f'{msg} added')
    else:
        await event.edit(f'{msg} already exist')


@register(outgoing=True, pattern="^.ignore(?: |$)(-?\\d+) (\\w+)")
async def remove_listener(event):
    """ Command for removing a filter """
    if not is_mongo_alive():
        await event.edit("`Database connections failing!`")
        return
    chat_id = event.pattern_match.group(1)
    keyword = event.pattern_match.group(2)
    if not chat_id or not chat_id:
        await event.edit("`You have to specify a chatid and a keyword!`")
        return

    if not await delete_listener(chat_id, keyword):
        await event.edit("`Filter `**{}**` doesn't exist on {}.`".format(keyword, chat_id))
    else:
        await event.edit(
            "`Filter `**{}**` was deleted successfully from {}`".format(keyword, chat_id))


@register(outgoing=True, pattern="^.listeners$")
async def listeners_active(event):
    """ For .listeners$ command, lists all of the active listeners. """
    if not is_mongo_alive():
        await event.edit("`Database connections failing!`")
        return

    transact = "`There are no listeners.`"
    listeners = await get_all_listeners()
    for listener in listeners:
        if transact == "`There are no listeners.`":
            transact = "Active listeners:\n"
            transact += " • **{}** - `{}`\n".format(listener["chat_id"],
                                                    listener["keyword"])
        else:
            transact += " • **{}** - `{}`\n".format(listener["chat_id"],
                                                    listener["keyword"])

    await event.edit(transact)


CMD_HELP.update({
    "listeners": [
        'Listeners', " - `.listeners`: List all active listeners in this chat.\n"
                     " - `.listen <chat_id> <keyword>`: Add a listener to this chat. "
                     "NOTE: listeners are case insensitive.\n"
                     " - `.ignore <chat_id> <keyword>`: Removes the listener.\n"
    ]
})
