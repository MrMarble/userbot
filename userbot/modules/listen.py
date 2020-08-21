import re

from userbot import is_mongo_alive, bot, BOTLOG_CHATID, CMD_HELP
from userbot.decorators import register
from userbot.modules.dbhelper import add_filter, get_listeners, delete_listener, get_all_listeners


@register(incoming=True, disable_errors=True)
async def filter_incoming_handler(handler):
    """ Checks if the incoming message contains handler of a filter """
    try:
        if not (await handler.get_sender()).bot:
            if not is_mongo_alive():
                await handler.edit("`Database connections failing!`")
                return

            filters = await get_listeners(handler.chat_id)
            if not filters:
                return
            for trigger in filters:
                pattern = r"( |^|[^\w])" + re.escape(
                    trigger["keyword"]) + r"( |$|[^\w])"
                if re.search(pattern, handler.text, flags=re.IGNORECASE):
                    await handler.reply(trigger["msg"])
                    await bot.forward_messages(BOTLOG_CHATID, handler)
                    return
    except AttributeError:
        pass


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

    msg = f"`Listen to `**{keyword}**` on chat `**{chat_id}**`"

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
        if transact == "`There are no filters in this chat.`":
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
