""" Userbot module containing userid, chatid commands"""
from telethon.tl import functions

from userbot import CMD_HELP, bot
from userbot.decorators import register


@register(outgoing=True, pattern="^.userid(?: |$)([\s\S]*)")
async def useridgetter(target):
    """ For .userid command, returns the ID of the target user. """

    username = target.pattern_match.group(1)
    if username:
        user = await bot(functions.users.GetFullUserRequest(username))
        user = user.user
    else:
        message = await target.get_reply_message()
        if message:
            if not message.forward:
                user = message.sender
            else:
                user = message.forward.sender
    if user:
        if user.username:
            name = "@" + user.username
        else:
            name = "**" + user.first_name + "**"
        await target.edit("**Name:** {} \n**User ID:** `{}`".format(
            name, user.id))


@register(outgoing=True, pattern="^.chatid$")
async def chatidgetter(chat):
    """ For .chatid, returns the ID of the chat you are in at that moment. """
    await chat.edit("Chat ID: `" + str(chat.chat_id) + "`")


CMD_HELP.update({
    "chat": [
        "Chat", " - `.chatid`: Fetch the current chat's ID.\n"
                " - `.userid`: Fetch the ID of the user in reply or the original author of a forwarded message.\n"
                " - `.userid <username>`: Fetch the ID of the provided username.\n"
    ]
})
