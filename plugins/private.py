from texts import start_msg, zmanim
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup
from plugins.markups import start, share
from database.database import db
from database.users import users
from config import bot_username
import asyncio


@Client.on_message(filters.command('start') & filters.private)
async def start_(_: Client, m: Message):
    if not await users.is_user_exist(m.from_user.id):
        await users.add_user(m.from_user.id)
    await m.reply_text(start_msg.format(m.from_user.first_name), reply_markup=start)


@Client.on_message(filters.command(['shabat', f'shabat{bot_username}']))
async def shabat(_, m: Message):
    send = await m.reply_text('בודק זמנים... אנא המתן ⌛️')
    await asyncio.sleep(1)
    await send.edit_text(zmanim, reply_markup=InlineKeyboardMarkup(share))


@Client.on_message(filters.command(['stats', 'start stats']) & filters.private)
async def stats(_: Client, m: Message):
    send = await m.reply_text('מחשב... אנא המתן ⌛️')
    total = await db.total_chat_count()

    await asyncio.sleep(1)
    text = "📊 **סך הכל קבוצות שומרות שבת בזכותי**: `{}`"
    await send.edit_text(text.format(total))


@Client.on_message(filters.private & filters.command('settings'))
async def pm_settings(_, m: Message):
    await m.reply_text("הפקודה הזאת לא עובדת בצ'אט פרטי. רק בקבוצה!")