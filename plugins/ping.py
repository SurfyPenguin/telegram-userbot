import asyncio
from ping3 import ping
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
from userbot import DCS, PREFIXES, AUTH_USERS
from time import perf_counter

async def do_ping(host) -> str:
    result = await asyncio.to_thread(lambda : ping(host)*1000)
    if result:
        return f"{result:.2f}"
    else:
        return "Timed Out"

# Ping data centres command
@Client.on_message(filters.command("pingdc", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def pingdc_command(_, message : Message):
    dc_info = ""
    for dc in DCS:
        dc_info += f"<pre language='DC{dc}'>{DCS[dc]["location"]} - {await do_ping(DCS[dc]["ip"])}ms</pre>"
    await message.reply(dc_info, quote = True, parse_mode = ParseMode.HTML)

# Ping client command
@Client.on_message(filters.command("ping", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def ping_command(_, message : Message):
    start = perf_counter()
    to_edit = await message.reply("**Pong!**")
    end = perf_counter()
    # await message.delete()
    await to_edit.edit_text(f"**Pong!** - `{(end - start) * 1000 :.2f}ms`")