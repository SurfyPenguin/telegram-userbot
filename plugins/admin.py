from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from pyrogram.errors import PeerIdInvalid, UsernameInvalid, UsernameNotOccupied, UserAdminInvalid, MessageDeleteForbidden, ChatAdminRequired
from userbot import CHUNK, PREFIXES, AUTH_USERS
from datetime import datetime
from userbot.main import app
from pyrogram.types import ChatPrivileges


PROMOTE =  ChatPrivileges(
    can_manage_chat=True,
    can_delete_messages=True,
    can_manage_video_chats=False,
    can_restrict_members=True,
    can_promote_members=False,
    can_change_info=False,
    can_post_messages=False,
    can_edit_messages=False,
    can_invite_users=True,
    can_pin_messages=True,
    can_manage_topics=True,
    can_post_stories=False,
    can_edit_stories=False,
    can_delete_stories=False,
    is_anonymous=False
)


DEMOTE = ChatPrivileges(
    can_manage_chat=False,
    can_delete_messages=False,
    can_manage_video_chats=False,
    can_restrict_members=False,
    can_promote_members=False,
    can_change_info=False,
    can_post_messages=False,
    can_edit_messages=False,
    can_invite_users=False,
    can_pin_messages=False,
    can_manage_topics=False,
    can_post_stories=False,
    can_edit_stories=False,
    can_delete_stories=False,
    is_anonymous=False
)

async def get_user(app : Client, message : Message):
    user = None
    if len(message.command) > 1 and (message.command[1].startswith("@") or message.command[1].isnumeric()):
        user = await app.get_users(message.command[1])

    elif message.reply_to_message:
        user = message.reply_to_message.from_user
    else:
        await message.reply("Provide a user")
    return user

# Purge func
async def purge(app : Client, message : Message) -> int:
    message_ids = [id for id in range(message.reply_to_message.id , message.id + 1)]
    deleted = 0
    # deletion in chunks
    for i in range(0, len(message_ids), CHUNK):
        deleted += await app.delete_messages(chat_id = message.chat.id, message_ids = message_ids[i:i+CHUNK+1])
    return deleted

# Purge command
@Client.on_message(filters.command("purge", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def purge_command(app : Client, message : Message) -> None:
    try:
        if message.reply_to_message:
            deleted = await purge(app, message)
            await message.reply(f"Deleted `{deleted}` messages")
        else:
            await message.reply("Please reply to a message", quote = True)

    except MessageDeleteForbidden:
        await message.reply("I don't have permissions to delete messages from other users")

# Silent purge command
@Client.on_message(filters.command("spurge", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def spurge_command(app : Client, message : Message) -> None:
    try:
        if message.reply_to_message:
            await purge(app, message)
        else:
            await message.reply("Please reply to a message", quote = True)
    except MessageDeleteForbidden:
        await message.reply("I don't have permissions to delete messages from other users")

@Client.on_message(filters.command("ban", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def ban_command(app : Client, message : Message):

    try:
        user = await get_user(app, message)
    
        if user:
            user_id = user.id
            await app.ban_chat_member(message.chat.id, user_id)
            await message.reply(f"Banned {user.mention(user.first_name)} from this chat")

    except PeerIdInvalid and UsernameInvalid and UsernameNotOccupied:
        await message.reply("Provide a valid user")
    except UserAdminInvalid:
        await message.reply("Can't ban an admin")
    except ChatAdminRequired:
        await message.reply("Hold on! I am not admin here")


@Client.on_message(filters.command("unban", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def unban_command(app : Client, message : Message):

    try:
        user = await get_user(app, message)
    
        if user:
            user_id = user.id
            await app.unban_chat_member(message.chat.id, user_id)
            await message.reply(f"Unbanned {user.mention(user.first_name)} from this chat")

    except PeerIdInvalid and UsernameInvalid and UsernameNotOccupied:
        await message.reply("Provide a valid user")
    except UserAdminInvalid:
        await message.reply("Can't unban an admin")
    except ChatAdminRequired:
        await message.reply("Hold on! I am not admin here")

@Client.on_message(filters.command("promote", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def promote_command(app : Client, message : Message):
    user = None

    try:
        if len(message.command) > 1 and (message.command[1].startswith("@") or message.command[1].isnumeric()):
            user = await app.get_users(message.command[1])
            tag = " ".join(message.command[2:])

        elif message.reply_to_message:
            user = message.reply_to_message.from_user
            tag = " ".join(message.command[1:])
            
        else:
            await message.reply("Provide a user")
        
        if user:
            await app.promote_chat_member(message.chat.id, user.id, title = tag, privileges= PROMOTE)
            await message.reply(f"Promoted! {user.mention(user.first_name)}")

    except PeerIdInvalid and UsernameInvalid and UsernameNotOccupied:
        await message.reply("Provide a valid user")
    except ChatAdminRequired:
        await message.reply("Are you sure I have the required permissions?")

@Client.on_message(filters.command("demote", prefixes= PREFIXES) & filters.user(AUTH_USERS))
async def demote_command(app : Client, message : Message):

    try:
        user = await get_user(app, message)
        
        if user:
            await app.promote_chat_member(message.chat.id, user.id, privileges= DEMOTE)
            await message.reply(f"Demoted! {user.mention(user.first_name)}")

    except PeerIdInvalid and UsernameInvalid and UsernameNotOccupied:
        await message.reply("Provide a valid user")
    except ChatAdminRequired:
        await message.reply("Are you sure I have the required permissions?")