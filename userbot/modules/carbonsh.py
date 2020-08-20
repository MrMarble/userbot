import os
import pathlib

import carbonsh
from telethon.events import NewMessage

from userbot import CMD_HELP, bot, LOGS
from userbot.decorators import register


@register(outgoing=True, pattern="^.carbon(?: |$)([\s\S]*)")
async def carbon_image(event: NewMessage):
    """Sends code as image"""
    code = event.pattern_match.group(1)
    carbon_path = pathlib.Path().absolute().joinpath('carbon', '')
    carbon_file = carbon_path.joinpath('carbon.png')

    if code:
        try:
            await event.edit("`Generating image...`")
            await carbonsh.code_to_file(code, carbonsh.Config(font_family=carbonsh.fonts.FIRA_CODE), carbon_path,
                                        headless=True)
            await bot.send_file(event.chat, str(carbon_file))  # TODO: This is broken sometimes
        except TypeError as err:
            LOGS.exception(err)
        finally:
            await event.delete()
            os.remove(carbon_file)


@register(outgoing=True, pattern="^.carbonurl(?: |$)([\s\S]*)")
async def carbon_url(event: NewMessage):
    """Sends code as url"""
    code = event.pattern_match.group(1)

    if code:
        url = carbonsh.code_to_url(code, carbonsh.Config(font_family=carbonsh.fonts.FIRA_CODE))
        await event.edit(url)


CMD_HELP.update({
    "carbonsh": [
        "Carbonsh",
        " - `.carbon <code>`: Send a beautiful image of code.\n"
        " - `.carbonurl <code>`: Sends a url containt the code.\n"
    ]
})
