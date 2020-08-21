from platform import python_version

from telethon import version

from userbot import CMD_HELP, is_mongo_alive
from userbot.decorators import register


@register(outgoing=True, pattern="^.alive$")
async def amireallyalive(alive):
    if not is_mongo_alive():
        db = "Mongo DB seems to be failing!"
    else:
        db = "Databases functioning normally!"

    await alive.edit("`"
                     "Userbot is alive and running!\n\n"
                     f"Telethon version: {version.__version__} \n"
                     f"Python: {python_version()} \n"
                     f"Database status: {db}\n"
                     "`")


CMD_HELP.update({
    "userbot": [
        "Userbot",
        " - `.alive`: Check if userbot is running.\n"
    ]
})
