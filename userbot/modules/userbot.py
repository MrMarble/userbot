from platform import python_version

from telethon import version

from userbot import CMD_HELP
from userbot.decorators import register


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    await alive.edit("`"
                     "Userbot is alive and running!\n\n"
                     f"Telethon version: {version.__version__} \n"
                     f"Python: {python_version()} \n"
                     "`")


CMD_HELP.update({
    "userbot": [
        "Userbot",
        " - `.alive`: Check if userbot is running.\n"
    ]
})
