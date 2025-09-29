# Pyrogram userbot

A simple telegram userbot made with pyrofork(mayuri) python library.

## Host locally
1. Create virtual environment and install requirements from `requirements.txt`.

```sh
pip install -r requirements.txt
```
2. Put API_ID and API_HASH in `.env`. Get API ID and hash from [here](https://my.telegram.org/auth) by creating an application if haven't already created.

3. Follow the instructions on the screen and run the userbot.

```sh
python3 main.py
```



## Commands
- Prefixes can be changed in `config.py`
- `?` -> __Admin commands__
- `!` -> __Music commands__
## Prefix: `?`
- __`/purge`__ - Send `?purge` while replying to a message.
- __`/info`__ - Send `?info` while replying to a message, or mentioning username `?info <username or id>`.
- __`/spurge`__ - Same as `?purge` except silent purge will not send number of deleted messages in chat.
- __`/ping`__ - Pings the chat in which `?ping` is sent. 
- __`/pingdc`__ - `?pingdc` Pings all the DCs (Data Centers) mentioned in pyrofork (mayuri).
- __`/alive`__ - `?alive` shows basic information like memory usage and uptime.
- __`/addfed`__ - Adds the current chat into the fed list in which `?fban` is to be sent.
- __`/rmfed`__ - Removes the current chat from the fed list.
- __`/fban`__ - `?fban <username or id> <reason>` will send `/fban` with the given reason in all the chats in fed list.
- __`/ban`__ - Either send the command by replying to a message or mentioning username. `?ban <username or id>`.
- __`/unban`__ - Same usage as `?ban`, except this command unbans the user.
- __`/promote`__ - Either send the command by replying to a message or mentioning username. `?promote <username or id>`.
- __`/demote`__ - Either send the command by replying to a message or mentioning username. `?demote <username or id>`.
## Prefix: `!`
- __`/play`__ - `!play <yt or yt-music link>` will start playing a song or play song replacing the current song.
- __`/add`__ - `!add <yt or yt-music link>` will add a song to the queue.
- __`/mute`__ - Mutes the music in voice chat.
- __`/unmute`__ - Unmutes the music in voice chat.
- __`/pause`__ - Pauses the music in voice chat.
- __`/resume`__ - Resume the music in voice chat.
- __`/leave`__ - `!leave` will forcefully leave the voice chat and queue will be cleared.

## Known Issues
`Database locked` : Common error faced when using the music commands.

## __No Progress__
I made this mini project to learn python as my first language. I no longer use telegram, so the purpose of this __project is over__.