""" Inizialitation. """

from logging import getLogger, basicConfig, INFO
from os import environ
from sys import version_info

from environs import Env, EnvValidationError
from telethon import TelegramClient
from telethon.sessions import StringSession

# Log configuration
basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            level=INFO)
LOGS = getLogger(__name__)

# Quit if python version is not compatible
if version_info[0] < 3 or version_info[1] < 6:
    LOGS.error("You MUST have a python version of at least 3.6."
               " Multiple features depend on this. Halting!")
    quit(1)

# Parse environment variables
env = Env()
env.read_env()

try:
    API_KEY: int = env.int('API_KEY', validate=lambda n: n != 0)
except EnvValidationError:
    LOGS.error("API key is invalid! Check your .env")
    quit(1)
try:
    API_HASH: str = env.str('API_HASH', validate=lambda n: len(n) > 0)
except EnvValidationError:
    LOGS.error("API Hash is invalid! Check your .env")
    quit(1)

STRING_SESSION: str = env.str('STRING_SESSION') or None

# Test variable
SEM_TEST = environ.get("SEMAPHORE", None)

# Instantiate Telethon
if STRING_SESSION:
    bot = TelegramClient(StringSession(STRING_SESSION), API_KEY, API_HASH)
else:
    bot = TelegramClient("userbot", API_KEY, API_HASH)
