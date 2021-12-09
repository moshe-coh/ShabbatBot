import os
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import InputUserDeactivated, UserIsBlocked, PeerIdInvalid
from pyrogram.types import Message
from database.users import users
from database.users import get_all_users
from config import admins


@Client.on_message(filters.command('broadcast') & filters.user(admins) & filters.private & filters.reply)
async def broadcast(bot: Client, m: Message):
    log_file = open('logger.txt', 'a+')
    total = await users.total_users_count()
    message = m.reply_to_message.message_id

    sent = 0
    failed = 0

    send = await bot.send_message(m.chat.id, f"**📣 starting broadcast to:** `{total} users`\nPlease Wait...")
    progress = await m.reply_text(f'**Message Sent To:** `{sent} users`')

    for user in await get_all_users():
        try:
            await bot.copy_message(user, m.chat.id, message)
            sent += 1
            await progress.edit_text(f'**Message Sent To:** `{sent} users`')
            await asyncio.sleep(.05)  # 20 messages per second (Limit: 30 messages per second)
        except InputUserDeactivated:
            await users.delete_user(user)
            log_file.write(f"user {user} is Deactivated\n")
            failed += 1
            continue
        except UserIsBlocked:
            await users.delete_user(user)
            log_file.write(f"user {user} Blocked your bot\n")
            failed += 1
            continue
        except PeerIdInvalid:
            await users.delete_user(user)
            log_file.write(f"user {user} IdInvalid\n")
            failed += 1
            continue
        except Exception as e:
            failed += 1
            log_file.write(f"can't sent to: {user} due: {str(e)}")
            continue

    await progress.delete()
    await send.edit_text(f"📣 Broadcast Completed\n\n🔸 **Total Users in db:** {total}\n\n🔹 Message sent to: {sent} users\n"
                         f"🔹 Failed to sent: {failed} users")
    log_file.close()
    try:
        await m.reply_document('logger.txt')
    except Exception as e:
        await m.reply_text(str(e))
    finally:
        os.remove('logger.txt')
