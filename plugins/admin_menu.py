from bot import allow, close
from database.database import db, get_all_chats
from database.users import users, get_all_users
from config import admins
from pyrogram import Client, filters
from pyrogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from pyrogram.errors import PeerIdInvalid
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler.jobstores.base import JobLookupError

from shabat import get_in, get_out

scheduler = AsyncIOScheduler()


@Client.on_message(filters.command('total') & filters.user(admins))
async def admin(_, m: Message):
    total = await db.total_chat_count()
    chat = await get_all_chats()
    total_users = await users.total_users_count()
    users_ids = await get_all_users()
    await m.reply_text(f"šø Total Chats {total}\n\nšø Chats id's:\n{chat}")
    await m.reply_text(f"šø Total Users {total_users}\n\nšø Chats id's:\n{users_ids}")

    await m.reply_text('Use `/info` +  id for get info about a group')


@Client.on_message(filters.command('info') & filters.user(admins))
async def info(_: Client, m: Message):
    if len(m.command) == 1:
        await m.reply_text('Usage: `/info` group id')
        return
    group = m.text.split()[1:]
    try:
        chat = await _.get_chat(' '.join(group))
        text = f"""
šø Group name: {chat.title}
šø Group link: {chat.invite_link}
šø Group Username: @{chat.username}
šø Group ID: {chat.id}

        """
        await m.reply_text(text)
    except PeerIdInvalid:
        await m.reply_text('Group Not Found')
    except Exception as e:
        await m.reply_text(str(e))


@Client.on_message(filters.command("add_sch") & filters.user(admins))
async def add_sch(client, m: Message):
    """add scheduler to close at holidays"""
    which_kb = ReplyKeyboardMarkup([
        [KeyboardButton("×”×××Ø×"), KeyboardButton("×¤×Ŗ×××")],
        [KeyboardButton("×××××")]
    ], resize_keyboard=True)

    date = await client.ask(m.chat.id, "×©×× ××Ŗ ××Ŗ××Ø×× ×©××Ø×¦×× × ××××”××£ ×Ŗ×××× ××¤××Ø×× day-month-year"
                                       "××××××: 20-10-2022")
    try:
        day, month, year = date.text.split("-")
    except ValueError:
        await m.reply_text("×¤××Ø×× ×©××× ā¹ļø")
        return

    which = await client.ask(m.chat.id, "×××× ×¤×¢××× ××××”××£ ×××Ŗ×××?", reply_markup=which_kb)
    if which.text == "×¤×Ŗ×××":
        name = f"open-{day}"
        hour_in, min_in = get_in().split(':')
        trigger = CronTrigger(year=year, month=month, day=day, hour=hour_in, minute=min_in)
        scheduler.add_job(allow, trigger=trigger, timezone='Asia/Jerusalem', id=name)
        await m.reply_text("×××©××× × ××”×¤× ×××¦×××! ×©× ×××©××× ×××: `{}`".format(name), reply_markup=ReplyKeyboardRemove())

    elif which.text == "×”×××Ø×":
        name = f"close-{day}"
        hour_in, min_in = get_out().split(':')
        trigger = CronTrigger(year=year, month=month, day=day, hour=hour_in, minute=min_in)
        scheduler.add_job(close, trigger=trigger, timezone='Asia/Jerusalem', id=name)
        await m.reply_text("×××©××× × ××”×¤× ×××¦×××! ×©× ×××©××× ×××: `{}`".format(name), reply_markup=ReplyKeyboardRemove())
    elif which.text == "×××××":
        await m.reply_text("×××× ×××¦×××!", reply_markup=ReplyKeyboardRemove())


@Client.on_message(filters.command('rem_sch') & filters.user(admins))
async def rem_sch(client, m: Message):
    which = await client.ask(m.chat.id, "×©×× ××Ŗ ×©× ×××©××× ×©××Ø××¦× × ×××”××Ø!")
    try:
        scheduler.remove_job(which.text)
        await m.reply_text("×××©××× {} ××××× ×××¦×××!".format(which.text))
    except JobLookupError:
        await m.reply_text("×©× ×××©××× ×× × ××¦× ā¹ļø")
