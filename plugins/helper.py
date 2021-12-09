from texts import HELP_MSG
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_message(filters.command(['help', 'start help']) & filters.private)
async def _help(client, message):
    await client.send_message(chat_id=message.chat.id,
                              text=HELP_MSG[1],
                              parse_mode="markdown",
                              reply_markup=InlineKeyboardMarkup(bt(1)))


def bt(pos):
    if pos == 1:
        button = [
            [InlineKeyboardButton(text='-->', callback_data="help+2")]
        ]
    elif pos == len(HELP_MSG) - 1:
        button = [
            [InlineKeyboardButton('📣 לערוץ העדכונים 📣', url='https://t.me/JewishBots'),
             InlineKeyboardButton(text="🗯 לקבוצת התמיכה 🗯", url="https://t.me/JewsSupport")],
            [InlineKeyboardButton(text='➕ להוספת הרובוט לקבוצה ➕', url="https://t.me/JewsShabatBot?startgroup=true")],
            [InlineKeyboardButton(text='<--', callback_data=f"help+{pos - 1}")]
        ]
    else:
        button = [
            [
                InlineKeyboardButton(text='<--', callback_data=f"help+{pos - 1}"),
                InlineKeyboardButton(text='-->', callback_data=f"help+{pos + 1}")
            ],
        ]
    return button
