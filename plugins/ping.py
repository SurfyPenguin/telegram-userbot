from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from helpers.ping import do_ping
from config import DCS, PREFIXES, AUTH_USERS
from time import perf_counter

# Ping data centres command
@Client.on_message(filters.command("pingdc", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def pingdc_command(_, message : Message):
    dc_info = ""
    for dc in DCS:
        dc_info += f"```{dc}\n{DCS[dc]["location"]} - {await do_ping(DCS[dc]["ip"])}ms```"
    await message.reply(dc_info, quote = True, parse_mode = ParseMode.MARKDOWN)

# Ping client command
@Client.on_message(filters.command("ping", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def ping_command(_, message : Message):
    start = perf_counter()
    to_edit = await message.reply("**Pong!**")
    end = perf_counter()
    # await message.delete()
    await to_edit.edit_text(f"**Pong!** - `{(end - start) * 1000 :.2f}ms`")