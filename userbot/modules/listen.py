import re
from datetime import timedelta

from userbot import is_mongo_alive, bot, BOTLOG_CHATID, CMD_HELP, LOGS
from userbot.decorators import register
from userbot.modules.dbhelper import add_filter, get_listeners, delete_listener, get_all_listeners
from userbot.modules.markdown import unmark


@register(incoming=True, outgoing=True, disable_errors=True)
async def filter_incoming_handler(handler):
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
                await parse_trigger(handler, sender, trigger["keyword"])

    except AttributeError as err:
        LOGS.exception(f'{handler.chat_id} - {err}')


async def parse_trigger(handler, sender, trigger):
    """ Aux function to generate trigger message """
    pattern = r"( |^|[^\w])" + re.escape(trigger) + r"( |$|[^\w])"
    text = unmark(handler.text)
    offset = 15
    if re.search(pattern, text, flags=re.IGNORECASE):
        chat_from = handler.chat if handler.chat else (
            await handler.get_chat())  # telegram MAY not send the chat entity
        chat_title = chat_from.title if hasattr(chat_from, 'title') else handler.chat_id

        # Sneak peak of the message
        trigger_index = text.find(trigger)
        sneak_peak = text
        if trigger_index > offset:
            sneak_peak = text[trigger_index - offset:trigger_index + len(trigger) + offset]
        else:
            sneak_peak = text[0: trigger_index + len(trigger) + offset]
        sneak_peak = sneak_peak.replace('\n', ' ')

        # Channel or group
        if handler.chat_id < 0:
            from_name = chat_title
            # We need to remove -100 from Channel ID
            if '-100' in str(handler.chat_id)[0:4]:
                from_link = f"https://t.me/c/{str(handler.chat_id)[4:]}/{handler.id}"
            else:
                from_link = f"https://t.me/c/{str(handler.chat_id)[1:]}/{handler.id}"

        # Private chat
        else:
            from_name = sender.first_name
            from_link = f"tg://openmessage?user_id={sender.id}&message_id={handler.id}"

        await bot.send_message(BOTLOG_CHATID, silent=False, schedule=timedelta(minutes=1),
                               parse_mode='HTML', message=(f"<b>HIT</b> <code>{trigger}</code>\n\n"
                                                           f"<b>FROM</b>: <a href='{from_link}'>{from_name}</a>\n"
                                                           f"<b>TEXT</b>: {sneak_peak}"))


@register(outgoing=True, pattern="^.listen(?: |$)(-?\\d+) ([\\w\\s]+)")
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


@register(outgoing=True, pattern="^.ignore(?: |$)(-?\\d+) ([\\w\\s]+)")
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
