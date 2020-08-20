from importlib import import_module

from telethon.errors.rpcerrorlist import PhoneNumberInvalidError

from userbot import LOGS, bot, SEM_TEST
from userbot.modules import ALL_MODULES

INVALID_PH = '\nERROR: The phone no. entered is incorrect' \
             '\n  Tip: Use country code (eg +44) along with num.' \
             '\n       Recheck your phone number'

try:
    bot.start()
except PhoneNumberInvalidError:
    print(INVALID_PH)
    exit(1)

for module_name in ALL_MODULES:
    imported_module = import_module("userbot.modules." + module_name)

LOGS.info("userbot is alive! Test it by typing .alive on any chat.")

if SEM_TEST:
    bot.disconnect()
else:
    bot.run_until_disconnected()
