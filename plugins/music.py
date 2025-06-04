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

class Stream:
    def __init__(self, app : Client):
        self.player = PyTgCalls(app)
        self.running = False

    async def start(self):
        if not self.running:
            await self.player.start()
            self.running = True

    async def stream(self, chat_id : int | str, link : str, audio_quality = AudioQuality.HIGH, video_quality= VideoQuality.HD_720p):
            await self.player.play(chat_id, 
                                MediaStream(
                                        link,
                                        audio_quality, 
                                        video_quality
                                    )
                                )
            await idle()

    async def command_handler(self, message : Message):
        action = message.command[0]
        chat_id = message.chat.id
        match action:
            case "leavecall":
                await self.player.leave_call(chat_id)
                await message.reply("`left call...`")
            case "pause":
                await self.player.pause(chat_id)
                await message.reply("`paused...`")
            case "resume":
                await self.player.resume(chat_id)
                await message.reply("`resumed...`")
            case "m":
                await self.player.mute(chat_id)
                await message.reply("`muted...`")
            case "um":
                await self.player.unmute(chat_id)
                await message.reply("`unmuted...`")
            case _:
                await message.reply("`Invalid media action`")

streamer = Stream(app)

@Client.on_message(filters.command("play", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def play_command(_, message : Message):
    await streamer.start()
    chat_id, link = message.chat.id, message.command[1]

    try:
        await streamer.stream(chat_id, link)
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
async def command_handler(_, message : Message):
    try:
        await streamer.command_handler(message)
    except exceptions.ClientNotStarted:
        print("--------Client not started yet--------")
    except exceptions.NotInCallError:
        await message.reply("Join a call first or use /play")