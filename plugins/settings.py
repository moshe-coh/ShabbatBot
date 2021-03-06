from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import MessageNotModified
from database.database import db


async def BaseSettings(m: Message):

    markup = [
        [InlineKeyboardButton("馃摐 讛讙讚专转 讛讜讚注讜转", callback_data="SetMessages")],
        [InlineKeyboardButton("馃柤 讛讙讚专转 转诪讜谞讜转", callback_data="SetPhotos")],
        [InlineKeyboardButton("馃挔 讛讙讚专转 讛专砖讗讜转", callback_data="SetPermissions")],
        [InlineKeyboardButton("鉁栵笍 住讙讜专", callback_data="close")]
    ]
    try:
        await m.edit(
            text="鈿欙笍 **讛讙讚专讜转 诇拽讘讜爪讛:** `{}`".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass


async def ShowMessages(m: Message, chat_id: int):
    shabat_notf = await db.get_send_notf(chat_id)
    notifications = await db.get_notifications(chat_id)
    markup = [
        [InlineKeyboardButton(f"讝诪谞讬 讻谞讬住转 砖讘转: {'ON 鉁?' if shabat_notf is True else 'OFF 鉂?'} ",callback_data="notf")],
        [InlineKeyboardButton(f" 讛讜讚注讜转 诇驻谞讬 讜讗讞专讬 砖讘转: {'ON 鉁?' if notifications is True else 'OFF 鉂?'}", callback_data="notifications")],
        [InlineKeyboardButton("鉁忥笍 讛讙讚专 讛讜讚注讛 砖转砖诇讞 诇驻谞讬 砖讘转", callback_data="setShabatText")],
        [InlineKeyboardButton("鉁忥笍 讛讙讚专 讛讜讚注讛 砖转砖诇讞 讘诪讜爪讗讬 砖讘转", callback_data="setWeekText")],
        [InlineKeyboardButton("馃摐 讛爪讙 讛讛讜讚注讛 砖转砖诇讞 诇驻谞讬 砖讘转", callback_data="showShabatText")],
        [InlineKeyboardButton("馃摐 讛爪讙 讛讛讜讚注讛 砖转砖诇讞 讘诪讜爪讗讬 砖讘转", callback_data="showWeekText")],
        [InlineKeyboardButton("鈫笍 讛讞讝专 诇讘专讬专转 诪讞讚诇", callback_data="rmShabatText")],
        [InlineKeyboardButton("讞讝讜专 诇讛讙讚专讜转 馃敊", callback_data="BaseSettings"),
         InlineKeyboardButton("鉁栵笍 住讙讜专", callback_data="close")]]

    try:
        await m.edit(
            text="鈿欙笍 **讛讙讚专转 讛讜讚注讜转 诇拽讘讜爪讛:** `{}`".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass


async def ShowPermissions(m: Message, chat_id: int):
    permissions = await db.get_permissions(chat_id)
    markup = [
        [InlineKeyboardButton("砖诇讬讞转 讛讜讚注讜转 讟拽住讟: ON 鉁?", callback_data="AlwaysOn")],
        [InlineKeyboardButton("砖诇讬讞转 诪讚讬讛 {}".format(f" {'ON 鉁?' if (permissions['can_send_media_messages'] is True) else 'OFF 鉂?'}"), callback_data="SetMedia")],
        [InlineKeyboardButton("砖诇讬讞转 诪讚讘拽讜转 {}".format(f" {'ON 鉁?' if (permissions['can_send_stickers'] is True) else 'OFF 鉂?'}"), callback_data="SetStickers")],
        [InlineKeyboardButton("砖诇讬讞转 讗谞讬诪爪讬讜转 {}".format(f" {'ON 鉁?' if (permissions['can_send_animations'] is True) else 'OFF 鉂?'}"), callback_data="SetAnimations")],
        [InlineKeyboardButton("砖诇讬讞转 诪砖讞拽讬诐 {}".format(f" {'ON 鉁?' if (permissions['can_send_games'] is True) else 'OFF 鉂?'}"), callback_data="SetGames")],
        [InlineKeyboardButton("砖诇讬讞转 讘讜讟讬诐 讗讬谞诇讬讬谉 {}".format(f" {'ON 鉁?' if (permissions['can_use_inline_bots'] is True) else 'OFF 鉂?'}"), callback_data="SetInline")],
        [InlineKeyboardButton("讛讜住驻转 转爪讜讙讛 诪拽讚讬诪讛 砖诇 拽讬砖讜专 {}".format(f" {'ON 鉁?' if (permissions['can_add_web_page_previews'] is True) else 'OFF 鉂?'}"), callback_data="SetWebPreview")],
        [InlineKeyboardButton("砖诇讬讞转 讞讬讚讜谞讬诐 {}".format(f" {'ON 鉁?' if (permissions['can_send_polls'] is True) else 'OFF 鉂?'}"), callback_data="SetPolls")],
        [InlineKeyboardButton("讞讝讜专 诇讛讙讚专讜转 馃敊", callback_data="BaseSettings"),
         InlineKeyboardButton("鉁栵笍 住讙讜专", callback_data="close")],
    ]
    try:
        await m.edit(
            text="鈿欙笍 **讛讙讚专转 讛专砖讗讜转 诇拽讘讜爪讛:** `{}` **诇驻转讬讞讛 讘诪讜爪讗讬 砖讘转:**".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass


async def ShowPhotos(m: Message):
    markup = [
        [InlineKeyboardButton("馃柤 讛讙讚专转 转诪讜谞讛 砖转砖诇讞 讘讻谞讬住转 砖讘转", callback_data="SetInPhoto")],
        [InlineKeyboardButton("馃柤 讛讙讚专转 转诪讜谞讛 砖转砖诇讞 讘诪讜爪讗讬 砖讘转", callback_data="SetOutPhoto")],
        [InlineKeyboardButton("讞讝讜专 诇讛讙讚专讜转 馃敊", callback_data="BaseSettings"),
         InlineKeyboardButton("鉁栵笍 住讙讜专", callback_data="close")]
    ]

    try:
        await m.edit(
            text="鈿欙笍 **讛讙讚专讜转 转诪讜谞讜转 诇拽讘讜爪讛:** `{}`".format(m.chat.title), reply_markup=InlineKeyboardMarkup(markup))
    except MessageNotModified:
        pass
