from main import app
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pytgcalls import PyTgCalls
from pytgcalls import idle
from pytgcalls.types import AudioQuality
from pytgcalls.types import MediaStream
from pytgcalls.types import VideoQuality
from config import PREFIXES, AUTH_USERS
from pytgcalls import exceptions

player = PyTgCalls(app)

running = False

async def video_play(chat, link):
    await player.play(chat,
            MediaStream(
            link,
            AudioQuality.HIGH,
            VideoQuality.SD_480p,
        ))
    await idle()

@Client.on_message(filters.command("play", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def video_command(_, message: Message):
    if len(message.command) < 2:
        await message.reply("Usage: /play <yt url>", quote=True, parse_mode=ParseMode.DISABLED)
        return
    chat_id, link = message.chat.id, message.command[1]
    global running
    if not running:
        await player.start()
        running = True
    try:
        await video_play(chat_id, link)

    except exceptions.ClientNotStarted:
        print("----Client not started yet----")
    except FileNotFoundError:
        await message.reply("File not found")
    except exceptions.NoAudioSourceFound:
        await message.reply("Audio source has no audio")
    except exceptions.NoVideoSourceFound:
        await message.reply("Video source has no video")
    except exceptions.YtDlpError:
        await message.reply("Unexpected Yt-Dlp error: check logs")

        

@Client.on_message(filters.command(["leavecall", "pause", "resume", "m", "um"], prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def playback_actions(_, message: Message):
    action = message.command[0]
    chat_id = message.chat.id
    try:
        match action:
            case "leavecall":
                await player.leave_call(chat_id)
                await message.reply("`left call...`")
            case "pause":
                await player.pause(chat_id)
                await message.reply("`paused...`")
            case "resume":
                await player.resume(chat_id)
                await message.reply("`resumed...`")
            case "m":
                await player.mute(chat_id)
                await message.reply("`muted...`")
            case "um":
                await player.unmute(chat_id)
                await message.reply("`unmuted...`")
            case _:
                await message.reply("`Invalid media action`")
  
    except exceptions.ClientNotStarted:
        print("--------Client not started yet--------")
    except exceptions.NotInCallError:
        await message.reply("Join a call first or use /play")
