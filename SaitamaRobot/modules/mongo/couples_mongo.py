from SaitamaRobot import db
from typing import Dict, List, Union

coupledb = db.couple

async def get_lovers(chat_id: int) -> Dict[str, dict]:
    lovers = await coupledb.find_one({"chat_id": chat_id})
    return lovers.get("couple", {})

async def get_couple(chat_id: int, date: str) -> Union[bool, dict]:
    lovers = await get_lovers(chat_id)
    return lovers.get(date, False)

async def save_couple(chat_id: int, date: str, couple: dict):
    async with coupledb:
        await coupledb.update_one(
            {"chat_id": chat_id},
            {"$set": {f"couple.{date}": couple}},
            upsert=True
        )
