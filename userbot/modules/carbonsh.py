import os
import pathlib

from carbonsh import code_to_file, code_to_url, Config, fonts
from telethon.events import NewMessage

from userbot import CMD_HELP, bot, LOGS
from userbot.decorators import register


@register(outgoing=True, pattern="^.carbon(?: |$)([\s\S]*)")
async def carbon_image(event: NewMessage):
    """Sends code as image"""
    code = event.pattern_match.group(1)
    carbon_path = pathlib.Path().absolute().joinpath('carbon', '')
    if not os.path.exists(carbon_path):
        os.mkdir(carbon_path)
    carbon_file = carbon_path.joinpath('carbon.png')

    if code:
        try:
            await event.edit("`Generating image...`")
            await code_to_file(code, Config(font_family=fonts.FIRA_CODE), carbon_path, headless=True,
                               executablePath='/usr/bin/google-chrome-stable', args=['--no-sandbox', '--disable-gpu'])
            await bot.send_file(event.input_chat, str(carbon_file))
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
        url = code_to_url(code, Config(font_family=fonts.FIRA_CODE))
        await event.edit(url)


CMD_HELP.update({
    "carbonsh": [
        "Carbonsh",
        " - `.carbon <code>`: Send a beautiful image of code.\n"
        " - `.carbonurl <code>`: Sends a url containt the code.\n"
    ]
})
