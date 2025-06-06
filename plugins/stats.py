from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import SlowmodeWait
from config import PREFIXES, AUTH_USERS, DCS
from helpers.ping import do_ping
import time
from datetime import datetime
from psutil import cpu_percent, virtual_memory


start_time = datetime.now()

async def get_usage():
    """
    Retuns cpu and memory usage in percent values
    """

    cpu_pc = cpu_percent()
    memory_pc = virtual_memory().percent

    return cpu_pc, memory_pc

@Client.on_message(filters.command("alive", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def uptime_command(_, message : Message):
    end_time = datetime.now()

    ping = await do_ping(DCS[message.chat.dc_id]["ip"])

    cpu, memory = await get_usage()

    uptime = end_time.replace(microsecond=0) - start_time.replace(microsecond=0)
    format = format = f"<pre language='status'>Alive! \nUptime - {uptime} \nPing - {ping}ms</pre><pre language='resources'>Cpu - {cpu}% \nMemory - {memory}%</pre>"
    
    await message.reply(format)