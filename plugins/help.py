from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from config import CHUNK, PREFIXES, AUTH_USERS

MESSAGE =  """🎋<b>Commands</b>

<i><b>🌟Admin</b></i>
• `/ban`
• `/unban`
• `/promote`
• `/demote`
• `/kick`

<i><b>👾Music</b></i>
• `/play`
• `/leave`
• `/m`
• `/um`
• `/pause`
• `/resume`

<i><b>🔅Federations</b></i>
• `/addfed`
• `/rmfed`
• `/fban`

<i><b>🧊Misc</b></i>
• `/ping`
• `/pingdc`
"""

@Client.on_message(filters.command("help", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def help_command(app : Client, message : Message) -> None:
    chat_id, topic_id = message.chat.id, message.message_thread_id
    await message.reply(MESSAGE)