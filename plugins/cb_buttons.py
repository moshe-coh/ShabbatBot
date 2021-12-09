from pyrogram import Client, filters
from pyrogram.errors import MessageNotModified, UserNotParticipant
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, Message, InputMediaPhoto
from asyncio.exceptions import TimeoutError
from database.database import db
from plugins.settings import BaseSettings, ShowMessages, ShowPermissions, ShowPhotos
from plugins.helper import bt
from plugins.markups import settings
from texts import HELP_MSG, good_shabat, good_week
from config import bot_username, log_channel

help_callback_filter = filters.create(lambda _, __, query: query.data.startswith('help+'))


@Client.on_callback_query(~help_callback_filter)
async def cb_buttons(client: Client, cb: CallbackQuery):
    chat = cb.message.chat.id
    permissions = await db.get_permissions(chat)
    try:
        get = await client.get_chat_member(chat, cb.from_user.id)
    except UserNotParticipant:
        await cb.answer('אירעה שגיאה!\nיתכן שזה בגלל שאתה לא נמצא בקבוצה הזאת...!')
        return
    except Exception as e:
        print(e)
        await cb.answer('אירעה שגיאה!')
        return

    if get.status not in ['creator', 'administrator']:
        await cb.answer('אתה לא מנהל בקבוצה הזאת...', show_alert=True)
        return

    if "SetMessages" in cb.data:
        await ShowMessages(cb.message, chat)
    elif "SetPermissions" in cb.data:
        await ShowPermissions(cb.message, chat)
    elif "SetPhotos" in cb.data:
        await ShowPhotos(cb.message)
    elif "BaseSettings" in cb.data:
        await BaseSettings(cb.message)

    elif "notf" in cb.data:
        notifications = await db.get_send_notf(chat)
        await db.set_notf_on(chat, send_notf=(False if (notifications is True) else True))
        await cb.answer("הוגדר בהצלחה ⚙️")
        await ShowMessages(cb.message, chat)

    elif "setShabatText" in cb.data:
        await cb.message.edit(
            "📄 השב על ההודעה הזאת עם טקסט שתרצה שישלח מידי ערב שבת לפני שהקבוצה נסגרת.\nאו השב /cancel לביטול", )
        try:
            event_: Message = await client.listen(chat, filters=filters.reply, timeout=300)
            if event_.text:
                if event_.text == "/cancel" or event_.text == f"/cancel{bot_username}":
                    await event_.delete(True)
                    await cb.message.edit("❌ בוטל בהצלחה", reply_markup=settings)
                else:
                    shabat_text = event_.text
                    await db.set_shabat_text(chat, shabat_text)
                    await client.send_message(log_channel,
                                              f"shabat-text in group {cb.message.chat.title} set as:\n{shabat_text}")
                    await cb.message.edit(
                        text="ההודעה הוגדרה בהצלחה.\n**ההודעה שתשלח היא:** {}".format(shabat_text),
                        reply_markup=settings)
        except TimeoutError:
            await cb.message.edit("עברו חמש דקות... יש לשלוח /settings שוב להגדרה מחדש... 😐")
    elif "rmShabatText" in cb.data:
        await db.set_shabat_text(chat, shabat_text=good_shabat)
        await db.set_week_text(chat, good_week=good_week)
        await cb.answer("↪️ הטקסט הוגדר כברירת מחדל!", show_alert=True)
        await BaseSettings(cb.message, )
    elif "showShabatText" in cb.data:
        shabat_text = await db.get_shabat_text(chat)
        await cb.message.edit("**ההודעה שתשלח בערב שבת היא:**\n{}".format(shabat_text), parse_mode="markdown",
                              reply_markup=settings)
    elif "setWeekText" in cb.data:
        await cb.message.edit(
            "📄 השב על ההודעה הזאת עם טקסט שתרצה שישלח מידי צאת השבת כשהקבוצה נפתחת.\nאו השב /cancel לביטול", )
        try:
            event_: Message = await client.listen(chat, filters=filters.reply, timeout=300)
            if event_.text:
                if event_.text == "/cancel" or event_.text == f"/cancel{bot_username}":
                    await event_.delete(True)
                    await cb.message.edit("❌ בוטל בהצלחה", reply_markup=settings)
                else:
                    week_text = event_.text
                    await db.set_week_text(chat, week_text)
                    await client.send_message(log_channel,
                                              f"week-text in group {cb.message.chat.title} set as:\n{week_text}")
                    await cb.message.edit(
                        text="ההודעה הוגדרה בהצלחה.\n**ההודעה שתשלח היא:** {}".format(week_text),
                        reply_markup=settings)
        except TimeoutError:
            await cb.message.edit("עברו חמש דקות... יש לשלוח /settings שוב להגדרה מחדש... 😐")

    elif "showWeekText" in cb.data:
        week = await db.get_week_text(chat)
        await cb.message.edit("**ההודעה שתשלח במוצאי שבת היא:**\n{}".format(week), parse_mode="markdown",
                              reply_markup=settings)

    elif "SetInPhoto" in cb.data:
        await cb.message.edit("שלח תמונה שתשלח לקבוצה בערב שבת.\nאו השב /cancel לביטול")
        try:
            event_: Message = await client.listen(chat, filters=filters.photo | filters.text, timeout=300)
            if event_.text:
                if event_.text == "/cancel" or event_.text == f"/cancel{bot_username}":
                    await event_.delete(True)
                    await cb.message.edit("❌ בוטל בהצלחה", reply_markup=settings)
            else:
                photo = event_.photo.file_id
                in_text = await db.get_shabat_text(chat)
                await db.set_photo_in(chat, photo)
                await cb.message.edit_media(media=InputMediaPhoto(media=str(photo), caption=in_text), reply_markup=settings)
        except TimeoutError:
            await cb.message.edit("עברו חמש דקות... יש לשלוח /settings שוב להגדרה מחדש... 😐")
    elif "SetOutPhoto" in cb.data:
        await cb.message.edit("שלח תמונה שתשלח לקבוצה במוצאי שבת.\nאו השב /cancel לביטול")
        try:
            event_: Message = await client.listen(chat, filters=filters.photo | filters.text, timeout=300)
            if event_.text:
                if event_.text == "/cancel" or event_.text == f"/cancel{bot_username}":
                    await event_.delete(True)
                    await cb.message.edit("❌ בוטל בהצלחה", reply_markup=settings)
            else:
                photo = event_.photo.file_id
                out_text = await db.get_week_text(chat)
                await db.set_photo_out(chat, photo)
                await cb.message.edit_media(media=InputMediaPhoto(media=str(photo), caption=out_text), reply_markup=settings)
        except TimeoutError:
            await cb.message.edit("עברו חמש דקות... יש לשלוח /settings שוב להגדרה מחדש... 😐")
    elif "notifications" in cb.data:
        current = await db.get_notifications(chat)
        await db.set_notifications(chat, True if current is False else False)
        await ShowMessages(cb.message, chat)

    elif "SetMedia" in cb.data:
        current = permissions['can_send_media_messages']
        await db.set_can_send_media_messages(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "SetStickers" in cb.data:
        current = permissions['can_send_stickers']
        await db.set_can_send_stickers(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "SetAnimations" in cb.data:
        current = permissions['can_send_animations']
        await db.set_can_send_animations(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "SetGames" in cb.data:
        current = permissions['can_send_games']
        await db.set_can_send_games(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "SetInline" in cb.data:
        current = permissions['can_use_inline_bots']
        await db.set_can_use_inline_bots(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "SetWebPreview" in cb.data:
        current = permissions['can_add_web_page_previews']
        await db.set_can_add_web_page_previews(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "SetPolls" in cb.data:
        current = permissions['can_send_polls']
        await db.set_can_send_polls(chat, True if current is False else False)
        await ShowPermissions(cb.message, chat)

    elif "AlwaysOn" in cb.data:
        await cb.answer("כדי שמשתמשי הקבוצה יוכלו לשלוח הודעות, ההגדרה הזאת תמיד תשאר פועלת...", show_alert=True)

    elif "close" in cb.data:
        try:
            await cb.message.reply_to_message.delete()
        except Exception as e:
            print(e)
        finally:
            await cb.message.delete()


@Client.on_callback_query(help_callback_filter)
async def help_answer(client, cb: CallbackQuery):
    chat_id = cb.from_user.id
    message_id = cb.message.message_id
    msg = int(cb.data.split('+')[1])
    try:
        await client.edit_message_text(chat_id=chat_id, message_id=message_id,
                                       text=HELP_MSG[msg], reply_markup=InlineKeyboardMarkup(bt(msg)))
    except MessageNotModified:
        await client.send_message(chat_id, '😳 אל תמחק את ההודעות שלי')
