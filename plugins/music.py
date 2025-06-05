from main import app
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.types import Message
from pytgcalls.types import AudioQuality, Update, StreamEnded, MediaStream, VideoQuality
from pyrogram.enums import ParseMode
from pytgcalls import PyTgCalls, idle, filters as fl
from config import PREFIXES, AUTH_USERS
from pytgcalls import exceptions
from yt_dlp import YoutubeDL

LIMIT = 40

ydl_opts = {
    "quiet" : True,
    "no_warnings" : True,
    "skip_download" : True,
    "format" : None,
    "gettitle" : True
}

ytdl = YoutubeDL(ydl_opts)

class Stream:
    def __init__(self, app : Client):
        self.app = app
        self.player = PyTgCalls(app)
        self.running = False
        self.queue = {}

    async def start(self):
        if not self.running:
            await self.player.start()
            self.running = True

    async def addqueue(self, chat_id, link):
        if chat_id not in self.queue.keys():
            self.queue[chat_id] = []
        title = await self.get_title(link)
        self.queue[chat_id].append([link, title])

    async def get_title(self, link):
        title = ytdl.extract_info(link, False).get("title")
        if len(title) >= LIMIT:
            return title[:LIMIT] + "..."
        else:
            return title

    async def stream(self, chat_id : int | str, link : str, audio_quality = AudioQuality.HIGH, video_quality= VideoQuality.HD_720p):
            await self.start()
            if chat_id not in self.queue.keys():
                self.queue[chat_id] = []

            await self.app.send_message(chat_id, f"Now streaming <a href='{link}'>{await self.get_title(link)}</a>", disable_web_page_preview=True)
            await self.player.play(chat_id, 
                                MediaStream(
                                        link,
                                        audio_quality, 
                                        video_quality
                                    )
                                )
            # await idle()

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

@streamer.player.on_update(fl.stream_end(stream_type=StreamEnded.Type.VIDEO))
async def handler(_ : PyTgCalls, update : StreamEnded):
    queue = streamer.queue[update.chat_id]
    # print(update)
    # print(queue)
    if len(queue) > 0:
        next = streamer.queue[update.chat_id][0]
        streamer.queue[update.chat_id].pop(0)

        await app.send_message(update.chat_id, f"Next playing <a href='{next[0]}'>{next[1]}</a> in 5 seconds...", disable_web_page_preview=True)
        await asyncio.sleep(5)

        await streamer.stream(update.chat_id, next[0])
        return
    
    if len(queue) == 0:
        await app.send_message(update.chat_id, "Video stream ended")

@Client.on_message(filters.command("play", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def play_command(_, message : Message):
    chat_id, link = message.chat.id, message.command[1]

    try:
        await streamer.stream(chat_id, link)

    except exceptions.ClientNotStarted:
        print("Client not started yet")
    except FileNotFoundError:
        await message.reply("File not found")
    except exceptions.NoAudioSourceFound:
        await message.reply("Audio source has no audio")
    except exceptions.NoVideoSourceFound:
        await message.reply("Video source has no video")
    except exceptions.YtDlpError:
        await message.reply("Unexpected Yt-Dlp error: check logs")
    except ChatAdminRequired:
        await message.reply("<b>I don't have permissions to manager video calls in this chat</b>")

@Client.on_message(filters.command(["leavecall", "pause", "resume", "m", "um"], prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def command_handler(_, message : Message):

    try:
        await streamer.command_handler(message)

    except exceptions.ClientNotStarted:
        print("--------Client not started yet--------")
    except exceptions.NotInCallError:
        await message.reply("Join a call first or use /play")

@Client.on_message(filters.command("add", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def add_command(_, message : Message):

    link = message.command[1]
    chat_id = message.chat.id

    if chat_id not in streamer.queue.keys():
        await streamer.stream(chat_id, link)
        return
    
    await message.reply(f"Adding link to queue...")
    await streamer.addqueue(message.chat.id, link)

@Client.on_message(filters.command("remove", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def remove_from_queue_command(_, message : Message):

    if len(message.command) != 2:
        await message.reply("usage: <code>/remove <queue-no></code>")
        return
    
    queue_id = int(message.command[1])
    if queue_id <= 0:
        await message.reply("Invalid queue number...")
        return
    
    streamer.queue[message.chat.id].pop(queue_id-1)
    await message.reply(f"Removed from queue: {queue_id}")

@Client.on_message(filters.command("queue", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def show_queue_command(_, message : Message):
    chat_id = message.chat.id
    
    if chat_id not in streamer.queue.keys():
        await message.reply("<b>Nothing is streaming in this chat at the moment</b>")
        return
    queue = streamer.queue[chat_id]

    if len(queue) == 0:
        await message.reply("<b>Queue is empty, use <code>/add yt-link</code> to add one</b>")
        return

    queue_format = "<b>Next in queue...</b>\n"
    for index, item in enumerate(queue):
        queue_format += f"<b>{index+1}.</b> <a href='{item[0]}'>{item[1]}</a>\n"
    await message.reply(queue_format, disable_web_page_preview=True)