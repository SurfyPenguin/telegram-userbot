# Telegram Userbot

## A multipurpose telegram userbot which can be used for moderation as well as playing music in telegram vc.

## Host Locally
Put API_ID and API_HASH in `.env`. Get API ID and hash from [here](https://my.telegram.org/auth) by creating an application if haven't already created.

---

* __Using Pip__
1. Clone repository
```bash
git clone https://github.com/SurfyPenguin/telegram-userbot.git
```
2. Create virutal environment
```bash
python3 -m venv .venv
```
3. Activate `.venv`
```bash
source .venv/bin/activate
```
4. Install dependencies
```bash
pip install .
```
5. Run project
```bash
python3 userbot/main.py
```
---

* __Using uv__
1. Clone repository
```bash
git clone https://github.com/SurfyPenguin/telegram-userbot.git
```
2. Create virtual environment
```bash
uv venv
```
3. Install dependencies
```bash
uv sync
```
4. Run project
```bash
uv run userbot/main.py
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