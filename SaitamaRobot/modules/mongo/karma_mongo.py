from SaitamaRobot import db
from typing import Dict, List, Union
import asyncio

karmadb = db.karma

async def get_karmas_count() -> Dict[str, int]:
    chats_count = 0
    karmas_count = 0

    async for chat in karmadb.find({"chat_id": {"$lt": 0}}):
        karmas_count += sum(entry["karma"] for entry in chat.get("karma", {}).values() if entry.get("karma", 0) > 0)
        chats_count += 1

    return {"chats_count": chats_count, "karmas_count": karmas_count}

async def get_karmas(chat_id: int) -> Dict[str, int]:
    karma_entry = await karmadb.find_one({"chat_id": chat_id})
    return karma_entry.get("karma", {}) if karma_entry else {}

async def get_karma(chat_id: int, name: str) -> Union[bool, int]:
    name = name.lower().strip()
    karmas = await get_karmas(chat_id)
    return karmas.get(name, False)

async def update_karma(chat_id: int, name: str, karma: int):
    name = name.lower().strip()
    async with karmadb:
        await karmadb.update_one(
            {"chat_id": chat_id},
            {"$set": {f"karma.{name}": karma}},
            upsert=True
        )

async def is_karma_on(chat_id: int) -> bool:
    chat_entry = await karmadb.find_one({"chat_id_toggle": chat_id})
    return bool(chat_entry)

async def karma_on(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if is_karma:
        return
    async with karmadb:
        await karmadb.delete_one({"chat_id_toggle": chat_id})

async def karma_off(chat_id: int):
    is_karma = await is_karma_on(chat_id)
    if not is_karma:
        return
    async with karmadb:
        await karmadb.insert_one({"chat_id_toggle": chat_id})

async def int_to_alpha(user_id: int) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return "".join(alphabet[int(i)] for i in str(user_id))

async def alpha_to_int(user_id_alphabet: str) -> int:
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    return int("".join(str(alphabet.index(i)) for i in user_id_alphabet))
