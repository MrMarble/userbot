""" Userbot's help command """

from userbot import CMD_HELP
from userbot.decorators import register


@register(outgoing=True, pattern="^.help(?: |$)(.*)")
async def help(event):
    """ For .help command"""
    args = event.pattern_match.group(1).lower()

    if args:
        if args in CMD_HELP:
            await event.edit(
                f"Here is some help for the **{CMD_HELP[args][0]}** module:\n\n"
                + str(CMD_HELP[args][1]))
        else:
            await event.edit(
                f"Help string for {args} not found! Type ```.help``` to see valid module names."
            )
    else:
        string = ""
        for i in CMD_HELP.values():
            string += f"`{str(i[0])}`, "
        string = string[:-2]
        await event.edit("Please specify which module you want help for!\n\n"
                         f"{string}")


CMD_HELP.update({
    "help": [
        "Help",
        "- `.help`: Gives a list of available commands"
    ]
})
