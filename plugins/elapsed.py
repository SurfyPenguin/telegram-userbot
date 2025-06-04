from pyrogram import Client, filters
from pyrogram.types import Message
from config import PREFIXES, AUTH_USERS, DCS
from helpers.ping import do_ping
from datetime import datetime

start_time = datetime.now()

@Client.on_message(filters.command("alive", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def uptime_command(_, message : Message):
    end_time = datetime.now()

    ping = await do_ping(DCS[message.chat.dc_id]["ip"])

    uptime = end_time.replace(microsecond=0) - start_time.replace(microsecond=0)
    format = f"```Status\nAlive! bot is currently running...\nUptime - `{uptime}`\nPing - {ping}ms```"

    await message.reply(format)