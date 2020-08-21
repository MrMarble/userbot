# Filters
from pymongo.cursor import Cursor

from userbot import MONGO


async def get_listeners(chatid) -> Cursor:
    return MONGO.listeners.find({'chat_id': chatid})


async def get_all_listeners():
    return MONGO.listeners.find()


async def get_listener(chatid, keyword):
    return MONGO.listeners.find_one({'chat_id': chatid, 'keyword': keyword})


async def add_filter(chatid, keyword):
    to_check = await get_listener(chatid, keyword)

    if not to_check:
        MONGO.listeners.insert_one({
            'chat_id': chatid,
            'keyword': keyword,
        })
        return True
    else:
        return False


async def delete_listener(chatid, keyword):
    to_check = await get_listener(chatid, keyword)

    if not to_check:
        return False
    else:
        MONGO.listeners.delete_one({
            '_id': to_check["_id"],
            'chat_id': to_check["chat_id"],
            'keyword': to_check["keyword"],
        })
        return True
