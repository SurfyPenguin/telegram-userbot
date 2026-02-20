from pyrogram import Client, filters
from pyrogram.types import Message
from userbot import PREFIXES, AUTH_USERS
# from helpers.chat import get_user
import json
import asyncio

SPACE = " "

with open("feds.json", "r") as file:
    feds = json.load(file)

async def get_json(file_path : str) -> dict:
    with open(file_path, "r") as file:
        data = json.load(file)
    return data

async def write_json(file_path , data) -> bool:
    with open(file_path, "w") as file:
        json.dump(data, file)

class FedManager:
    def __init__(self, file_path = "feds.json"):
        self.file_path = file_path
        self._cache = feds
        self._lock = asyncio.Lock()


    async def load(self):
        self._cache = await get_json(self.file_path)


    async def save(self):
        await write_json(self.file_path, self._cache)


    async def add(self, chat_id, topic_id):
        async with self._lock:
            self._cache[chat_id] = {"topic_id": topic_id}
            await self.save()

    
    async def remove(self, chat_id):
        async with self._lock:
            self._cache.pop(str(chat_id))
            await self.save()

    
    async def get_feds(self):
        return self._cache
    

fed_manager = FedManager()


async def fban(app : Client, message : Message) -> None:

    # chat id and topic id retrieval
    command = message.command
    if len(command) < 3:
        await message.reply("Invalid Usage!", quote= True)
        return
    
    user, reason = message.command[1], SPACE.join(command[2:])
    fban_message = f"/fban {user} {reason}"

    feds = await fed_manager.get_feds()
    tasks = [
        app.send_message(
            text = fban_message,
            chat_id = fed,
            message_thread_id= feds[fed]["topic_id"],
            disable_web_page_preview= True
            ) 
        for fed in feds
    ]

    await asyncio.gather(*tasks, return_exceptions= True)
    await message.reply(f"Banned in **{len(feds)}** federations", quote = True)

@Client.on_message(filters.command("fban", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def fban_command(app : Client, message: Message):
    await fban(app, message)


@Client.on_message(filters.command("addfed", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def addfed_command(_, message : Message) -> None:
    chat_id , topic_id = str(message.chat.id), message.message_thread_id
    await fed_manager.add(chat_id, topic_id)
    await message.reply("Added this chat to federations", quote = True)
    

@Client.on_message(filters.command("rmfed", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def rmfed_command(_, message : Message):
    chat_id = str(message.chat.id)
    await fed_manager.remove(chat_id)
    await message.reply("Removed this chat from federations", quote = True)

