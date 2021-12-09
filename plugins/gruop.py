from pyrogram import Client, filters
from pyrogram.types import Message
from database.database import db
import asyncio
import config
from plugins.markups import start, start_help, start_stats
from plugins.settings import BaseSettings


@Client.on_message(filters.group & filters.command(['add', f'add{config.bot_username}']))
async def add_chat(client: Client, m: Message):
    user_id = m.from_user.id
    user = await client.get_chat_member(m.chat.id, user_id)
    if user.status in ['creator', 'administrator']:
        if not await db.is_chat_exist(m.chat.id):
            chat = await client.get_chat(m.chat.id)
            send = await m.reply_text('מוסיף... אנא המתן!')
            me_status = await client.get_chat_member(m.chat.id, config.bot_username)
            if not me_status.can_restrict_members:
                return await send.edit_text('מסתבר ששכחת להוסיף לי הרשאות מתאימות.. הוסף אותי כמנהל ונסה שנית!')
            await asyncio.sleep(2)
            await send.edit_text('טוען את פרטי הקבוצה\nשם: {}\nid: {}'.format(chat.title, chat.id))
            await asyncio.sleep(3)
            await db.add_chat(m.chat.id)
            await send.edit_text('הקבוצה נוספה בהצלחה!\n💎 כעת באפשרותכם לשלוח /settings על מנת להגדיר אותי...')
            await client.send_message(config.log_channel, f'#new_chat!\n\n{chat.title}\nLink: {chat.invite_link}')
        elif await db.is_chat_exist(m.chat.id):
            return await m.reply_text('הקבוצה כבר בבסיס נתונים!')
    elif user.status not in ['administrator', 'creator']:
        send = await m.reply_text('אין לך הרשאות לפקודה זאת!')
        await asyncio.sleep(5)
        await send.delete()


@Client.on_message(filters.group & filters.command(['remove', f'remove{config.bot_username}']))
async def remove_chat(client: Client, m: Message):
    if not await db.is_chat_exist(m.chat.id):
        await m.reply_text('הקבוצה לא נמצאת בבסיס נתונים שלי!')
        return
    user = await client.get_chat_member(m.chat.id, m.from_user.id)
    if user.status in ['creator', 'administrator']:
        await db.delete_chat(m.chat.id)
        await m.reply_text('הקבוצה הוסרה בהצלחה! אני עוזב את הקבוצה...')
        await client.send_message(config.log_channel, f'chat {m.chat.title} removed!')
        await m.chat.leave()
    elif user.status not in ['administrator', 'creator']:
        send = await m.reply_text('{} אין לך הרשאות לפקודה זאת!'.format(m.from_user.mention))
        await asyncio.sleep(10)
        await send.delete()


@Client.on_message(filters.group & filters.command(['settings', f'settings{config.bot_username}']))
async def settings(_, m: Message):
    get = await _.get_chat_member(m.chat.id, m.from_user.id)
    if get.status in ['creator', 'administrator']:
        if not await db.is_chat_exist(m.chat.id):
            await db.add_chat(m.chat.id)
        editable = await m.reply_text("אנא המתן...", quote=True)
        await BaseSettings(editable)
    else:
        send = await m.reply_text('אתה לא מנהל בקבוצה הזאת!')
        await asyncio.sleep(10)
        await send.delete()


@Client.on_message(filters.group & filters.command(['start', f'start{config.bot_username}']))
async def start_(_: Client, m: Message):
    chat = await _.get_chat(m.chat.id)
    text = f" תודה שהוספתם אותי לקבוצה {chat.title}\n\nשלח /add על מנת ש{chat.title} תשמר " \
           f"בבסיס נתונים ותסגר בשבת ➕" \
           f"אל תשכח לשלוח /settings על מנת להתאים אישית את ההגדרות ברובוט"
    await m.reply_text(text, reply_markup=start)


@Client.on_message(filters.group & filters.command(['help', f'help{config.bot_username}']))
async def gp_help(_: Client, m: Message):
    await m.reply_text('{} תלחץ על בכפתור שלמטה למעבר לתפריט העזרה'.format(m.from_user.mention),
                       reply_markup=start_help)


@Client.on_message(filters.group & filters.command(['stats', f'stats{config.bot_username}']))
async def gp_stats(_, m: Message):
    await m.reply_text('{} תלחץ על בכפתור שלמטה למעבר לתפריט העזרה'.format(m.from_user.mention),
                       reply_markup=start_stats)
