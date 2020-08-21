# Filters
from userbot import MONGO


async def get_filters(chatid):
    return MONGO.filters.find({'chat_id': chatid})

async def get_all_filters():
    return MONGO.filters.find()

async def get_filter(chatid, keyword):
    return MONGO.filters.find_one({'chat_id': chatid, 'keyword': keyword})


async def add_filter(chatid, keyword, msg):
    to_check = await get_filter(chatid, keyword)

    if not to_check:
        MONGO.filters.insert_one({
            'chat_id': chatid,
            'keyword': keyword,
        })
        return True
    else:
        return False


async def delete_filter(chatid, keyword):
    to_check = await get_filter(chatid, keyword)

    if not to_check:
        return False
    else:
        MONGO.filters.delete_one({
            '_id': to_check["_id"],
            'chat_id': to_check["chat_id"],
            'keyword': to_check["keyword"],
        })
        return True
