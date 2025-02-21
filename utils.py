import asyncio
import logging
from pyrogram.errors import FloodWait, InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from database.db import db


from pyrogram import Client

async def get_invite_link(client: Client, channel_id: str):
    """Private channel ka invite link generate karega"""
    try:
        return await client.export_chat_invite_link(channel_id)
    except Exception as e:
        print(f"Error generating invite link: {e}")
        return None

async def is_subscribed(client: Client, user_id: int, channel_id: str):
    """Check if user is subscribed to the force join channel"""
    try:
        member = await client.get_chat_member(channel_id, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception:
        return False  # If error, assume not subscribed



async def broadcast_messages(user_id, message):
    try:
        await message.copy(chat_id=user_id)
        return True, "Success"
    except FloodWait as e:
        await asyncio.sleep(e.x)
        return await broadcast_messages(user_id, message)
    except InputUserDeactivated:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id}-Removed from Database, since deleted account.")
        return False, "Deleted"
    except UserIsBlocked:
        logging.info(f"{user_id} -Blocked the bot.")
        return False, "Blocked"
    except PeerIdInvalid:
        await db.delete_user(int(user_id))
        logging.info(f"{user_id} - PeerIdInvalid")
        return False, "Error"
    except Exception as e:
        return False, "Error"
