from main import app
import asyncio
from pytgcalls import PyTgCalls, idle, filters as fl, exceptions
from config import MUSIC_USERS , TITLE_LIMIT, MUSIC_PREFIXES
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode, ChatMemberStatus
from pytgcalls.types import MediaStream, AudioQuality, VideoQuality, StreamEnded
from pyrogram.errors import ChatAdminRequired
from yt_dlp import YoutubeDL

ydl_opts = {
    "quiet" : True,
    "no_warnings" : True,
    "skip_download" : True,
    "format" : None,
    "gettitle" : True
}

class Streamer:
    
    def __init__(self, app : Client):
        self._app = app
        self.player = PyTgCalls(app)
        self._running = False
        self.queue = {}

    async def start(self):
        if not self._running:
            await self.player.start()
            self._running = True

    def get_title(self, link):
        with YoutubeDL(ydl_opts) as ytdl:
            title = ytdl.extract_info(link).get("title")
        return title[:TITLE_LIMIT] + "..." if len(title) >= TITLE_LIMIT else title

    async def add_queue(self, chat_id, link):
        if chat_id not in self.queue.keys():
            self.queue[chat_id] = []
        title = await asyncio.to_thread(self.get_title, link)
        self.queue[chat_id].append([title, link])

    async def stream(self, chat_id, audio_quality = AudioQuality.MEDIUM, video_quality = VideoQuality.SD_360p):

        title, link = self.queue[chat_id][0]

        await self.start()
        await self._app.send_message(chat_id, f"<b>Now streaming <a href='{link}'>{title}</a></b>", disable_web_page_preview = True)

        if "music.youtube.com" in link:
            link = link.replace("music.youtube.com", "youtube.com")
            await self.player.play(
                chat_id = chat_id,
                stream = MediaStream(
                    media_path = link,
                    audio_parameters = audio_quality,
                    video_flags = MediaStream.Flags.IGNORE,
                ) 
            )

        await self.player.play(
            chat_id = chat_id,
            stream = MediaStream(
                media_path = link,
                audio_parameters = audio_quality,
                video_parameters = video_quality, 
            ) 
        )
    
    async def action_handler(self, message : Message):
        action = message.command[0]
        chat_id = message.chat.id
        match action:
            case "leave":
                self.queue[chat_id] = []
                await self.player.leave_call(chat_id)
                await message.reply("<i>left call...</i>")

            case "pause":
                await self.player.pause(chat_id)
                await message.reply("<i>paused...</i>")

            case "resume":
                await self.player.resume(chat_id)
                await message.reply("<i>resumed...</i>")

            case "mute":
                await self.player.mute(chat_id)
                await message.reply("<i>muted...</i>")

            case "unmute":
                await self.player.unmute(chat_id)
                await message.reply("<i>unmuted...</i>")

            case _:
                await message.reply("<i>Invalid media action<i>") # won't reach this case but anyways

streamer = Streamer(app)

@Client.on_message(filters.command("play", prefixes = MUSIC_PREFIXES) & filters.user(MUSIC_USERS))
async def play_command(app : Client, message : Message):

    chat_id = message.chat.id
    chat_member = await app.get_chat_member(chat_id, "me")

    if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
        await message.reply("<b>I'm not admin in this chat</b>")
        return
    
    if not chat_member.privileges.can_manage_video_chats:
        await message.reply("<b>I don't have permissions to manage video chats")
        return

    if len(message.command) != 2:
        await message.reply("<b>Usage <code>/play yt-link</code></b>", parse_mode = ParseMode.HTML)
        return
    
    link = message.command[1]
    try:
        if chat_id in streamer.queue.keys():

            if len(streamer.queue[chat_id]) > 0:

                title = streamer.get_title(link)
                streamer.queue[chat_id][0] = [title, link]

                await streamer.stream(chat_id)
                return
        
        await streamer.add_queue(chat_id, link)
        await streamer.stream(chat_id)
            

    except exceptions.ClientNotStarted:
        await message.reply("<b>Client not started yet</b>")
    except FileNotFoundError:
        await message.reply("<b>File not found</b>")
    except exceptions.NoAudioSourceFound:
        await message.reply("<b>Audio source has no audio</b>")
    except exceptions.NoVideoSourceFound:
        await message.reply("<b>Video source has no video</b>")
    except exceptions.YtDlpError:
        await message.reply("<b>Unexpected Yt-Dlp error: check logs</b>")
    except ChatAdminRequired:
        await message.reply("<b>I don't have permissions to manage video calls in this chat</b>")

@Client.on_message(filters.command("add", prefixes = MUSIC_PREFIXES) & filters.user(MUSIC_USERS))
async def add_command(app : Client, message : Message):
    chat_id = message.chat.id

    if len(message.command) != 2:
        await message.reply("<b>Usage: <code>/add yt-link</code></b>")
        return
    
    if message.chat.id not in streamer.queue.keys():
        chat_member = await app.get_chat_member(chat_id, "me")

        if chat_member.status not in [ChatMemberStatus.ADMINISTRATOR, ChatMemberStatus.OWNER]:
            await message.reply("<b>I'm not admin in this chat</b>")
            return
    
        if not chat_member.privileges.can_manage_video_chats:
            await message.reply("<b>I don't have permissions to manage video chats")
            return
        
        try:
            await streamer.add_queue(chat_id, message.command[1])
            await streamer.stream(chat_id)

        except exceptions.ClientNotStarted:
            await message.reply("<b>Client not started yet</b>")
        except FileNotFoundError:
            await message.reply("<b>File not found</b>")
        except exceptions.NoAudioSourceFound:
            await message.reply("<b>Audio source has no audio</b>")
        except exceptions.NoVideoSourceFound:
            await message.reply("<b>Video source has no video</b>")
        except exceptions.YtDlpError:
            await message.reply("<b>Unexpected Yt-Dlp error: check logs</b>")
        except ChatAdminRequired:
            await message.reply("<b>I don't have permissions to manage video calls in this chat</b>")
        return

    await message.reply("<b>Adding to queue...</b>")
    await streamer.add_queue(message.chat.id, message.command[1])


@Client.on_message(filters.command("queue", prefixes = MUSIC_PREFIXES) & filters.user(MUSIC_USERS))
async def show_queue_command(_, message : Message):
    chat_id = message.chat.id
    if chat_id not in streamer.queue.keys():
        await message.reply("<b>Nothing is streaming at the moment, use <code>/play yt-link</code> to start</b>")
        return
    
    queue = streamer.queue[chat_id]
    if len(queue) == 0:
        await message.reply("<b>Queue is empty...</b>")
        return
    
    queue_format = ""
    for index, item in enumerate(queue):
        if index == 0:
            queue_format += f"<b>Currently Playing:\n{index}. <a href='{item[1]}'>{item[0]}</a></b>\n\n"
            continue
        if index == 1:
            queue_format += f"<b>Next in queue:</b>\n"
        queue_format += f"<b>{index}. <a href='{item[1]}'>{item[0]}</a></b>\n"
    
    await message.reply(queue_format, disable_web_page_preview = True)

@Client.on_message(filters.command("remove", prefixes = MUSIC_PREFIXES) & filters.user(MUSIC_USERS))
async def remove_command(_, message : Message):
    chat_id = message.chat.id
    if chat_id not in streamer.queue.keys():
        await message.reply("<b>Nothing is streaming at the moment, use <code>/play yt-link</code> to start</b>")
        return

    if len(message.command) != 2:
        await message.reply("<b>Usage: <code>/remove queue_no</code></b>")
        return
    
    queue_id = int(message.command[1])
    if queue_id <= 0:
        await message.reply("<b>Invalid queue id</b>")
        return
    
    streamer.queue[chat_id].pop(queue_id)
    await message.reply(f"<b>Removed from queue: {queue_id}</b>")

@Client.on_message(filters.command("skip", prefixes = MUSIC_PREFIXES) & filters.user(MUSIC_USERS))
async def skip_command(_, message : Message):
    chat_id = message.chat.id
    if chat_id not in streamer.queue.keys():
        await message.reply("<b>Nothing is streaming at the moment, use <code>/play yt-link</code> to start</b>")
        return
    
    if len(streamer.queue[chat_id]) == 0:
        await message.reply("<b>Queue is empty...</b>")
        return
    
    if len(streamer.queue[chat_id]) == 1:
        await message.reply("<b>Can't skip, theres nothing next in queue.\nUse <code>/leave</code> instead to end the stream</b>")
        return
    
    streamer.queue[chat_id].pop(0)
    queue = streamer.queue[chat_id]
    if len(queue) == 0:
        await app.send_message(chat_id, f"<b>Stream Ended</b>")
        return
    
    try:
        await streamer.stream(chat_id)

    except exceptions.ClientNotStarted:
        await app.send_message(chat_id, "<b>Client not started yet</b>")
    except FileNotFoundError:
        await app.send_message(chat_id, "<b>File not found</b>")
    except exceptions.NoAudioSourceFound:
        await app.send_message(chat_id, "<b>Audio source has no audio</b>")
    except exceptions.NoVideoSourceFound:
        await app.send_message(chat_id, "<b>Video source has no video</b>")
    except exceptions.YtDlpError:
        await app.send_message(chat_id, "<b>Unexpected Yt-Dlp error: check logs</b>")
    except ChatAdminRequired:
        await app.send_message(chat_id, "<b>I don't have permissions to manage video calls in this chat</b>")


@streamer.player.on_update(fl.stream_end(stream_type=StreamEnded.Type.VIDEO))
async def handler(_ : PyTgCalls, update : StreamEnded):
    chat_id = update.chat_id
    streamer.queue[chat_id].pop(0)
    queue = streamer.queue[chat_id]

    if len(queue) == 0:
        await app.send_message(chat_id, f"<b>Stream Ended</b>")
        return
    
    await app.send_message(chat_id, f"<b>Next streaming <a href='{queue[0][1]}'>{queue[0][0]}</a> in 5 seconds...</b>", disable_web_page_preview = True)
    await asyncio.sleep(5)

    try:
        await streamer.stream(chat_id)

    except exceptions.ClientNotStarted:
        await app.send_message(chat_id, "<b>Client not started yet</b>")
    except FileNotFoundError:
        await app.send_message(chat_id, "<b>File not found</b>")
    except exceptions.NoAudioSourceFound:
        await app.send_message(chat_id, "<b>Audio source has no audio</b>")
    except exceptions.NoVideoSourceFound:
        await app.send_message(chat_id, "<b>Video source has no video</b>")
    except exceptions.YtDlpError:
        await app.send_message(chat_id, "<b>Unexpected Yt-Dlp error: check logs</b>")
    except ChatAdminRequired:
        await app.send_message(chat_id, "<b>I don't have permissions to manage video calls in this chat</b>")
    

@Client.on_message(filters.command(["leave", "pause", "resume", "mute", "unmute"], prefixes= MUSIC_PREFIXES) & filters.user(MUSIC_USERS))
async def command_handler(_, message : Message):

    try:
        await streamer.action_handler(message)

    except exceptions.ClientNotStarted:
        await message.reply("<b>Client not started yet</b>")
    except exceptions.NotInCallError:
        await message.reply("<b>Join a call first or use /play</b>")