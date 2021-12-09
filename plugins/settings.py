from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified
from database.database import db


async def BaseSettings(m: Message):

    markup = [
        [InlineKeyboardButton("📜 הגדרת הודעות", callback_data="SetMessages")],
        [InlineKeyboardButton("🖼 הגדרת תמונות", callback_data="SetPhotos")],
        [InlineKeyboardButton("💠 הגדרת הרשאות", callback_data="SetPermissions")],
        [InlineKeyboardButton("✖️ סגור", callback_data="close")]
    ]
    try:
        await m.edit(
            text="⚙️ **הגדרות לקבוצה:** `{}`".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass


async def ShowMessages(m: Message, chat_id: int):
    shabat_notf = await db.get_send_notf(chat_id)
    notifications = await db.get_notifications(chat_id)
    markup = [
        [InlineKeyboardButton(f"זמני כניסת שבת: {'ON ✅' if shabat_notf is True else 'OFF ❌'} ",callback_data="notf")],
        [InlineKeyboardButton(f" הודעות לפני ואחרי שבת: {'ON ✅' if notifications is True else 'OFF ❌'}", callback_data="notifications")],
        [InlineKeyboardButton("✏️ הגדר הודעה שתשלח לפני שבת", callback_data="setShabatText")],
        [InlineKeyboardButton("✏️ הגדר הודעה שתשלח במוצאי שבת", callback_data="setWeekText")],
        [InlineKeyboardButton("📜 הצג ההודעה שתשלח לפני שבת", callback_data="showShabatText")],
        [InlineKeyboardButton("📜 הצג ההודעה שתשלח במוצאי שבת", callback_data="showWeekText")],
        [InlineKeyboardButton("↪️ החזר לברירת מחדל", callback_data="rmShabatText")],
        [InlineKeyboardButton("חזור להגדרות 🔙", callback_data="BaseSettings"),
         InlineKeyboardButton("✖️ סגור", callback_data="close")]]

    try:
        await m.edit(
            text="⚙️ **הגדרת הודעות לקבוצה:** `{}`".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass


async def ShowPermissions(m: Message, chat_id: int):
    permissions = await db.get_permissions(chat_id)
    markup = [
        [InlineKeyboardButton("שליחת הודעות טקסט: ON ✅", callback_data="AlwaysOn")],
        [InlineKeyboardButton("שליחת מדיה {}".format(f" {'ON ✅' if (permissions['can_send_media_messages'] is True) else 'OFF ❌'}"), callback_data="SetMedia")],
        [InlineKeyboardButton("שליחת מדבקות {}".format(f" {'ON ✅' if (permissions['can_send_stickers'] is True) else 'OFF ❌'}"), callback_data="SetStickers")],
        [InlineKeyboardButton("שליחת אנימציות {}".format(f" {'ON ✅' if (permissions['can_send_animations'] is True) else 'OFF ❌'}"), callback_data="SetAnimations")],
        [InlineKeyboardButton("שליחת משחקים {}".format(f" {'ON ✅' if (permissions['can_send_games'] is True) else 'OFF ❌'}"), callback_data="SetGames")],
        [InlineKeyboardButton("שליחת בוטים אינליין {}".format(f" {'ON ✅' if (permissions['can_use_inline_bots'] is True) else 'OFF ❌'}"), callback_data="SetInline")],
        [InlineKeyboardButton("הוספת תצוגה מקדימה של קישור {}".format(f" {'ON ✅' if (permissions['can_add_web_page_previews'] is True) else 'OFF ❌'}"), callback_data="SetWebPreview")],
        [InlineKeyboardButton("שליחת חידונים {}".format(f" {'ON ✅' if (permissions['can_send_polls'] is True) else 'OFF ❌'}"), callback_data="SetPolls")],
        [InlineKeyboardButton("חזור להגדרות 🔙", callback_data="BaseSettings"),
         InlineKeyboardButton("✖️ סגור", callback_data="close")],
    ]
    try:
        await m.edit(
            text="⚙️ **הגדרת הרשאות לקבוצה:** `{}` **לפתיחה במוצאי שבת:**".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass


async def ShowPhotos(m: Message):
    markup = [
        [InlineKeyboardButton("🖼 הגדרת תמונה שתשלח בכניסת שבת", callback_data="SetInPhoto")],
        [InlineKeyboardButton("🖼 הגדרת תמונה שתשלח במוצאי שבת", callback_data="SetOutPhoto")],
        [InlineKeyboardButton("חזור להגדרות 🔙", callback_data="BaseSettings"),
         InlineKeyboardButton("✖️ סגור", callback_data="close")]
    ]

    try:
        await m.edit(
            text="⚙️ **הגדרות תמונות לקבוצה:** `{}`".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass
