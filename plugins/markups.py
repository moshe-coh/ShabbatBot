from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent
from pyrogram import Client
from texts import zmanim

start = InlineKeyboardMarkup([[InlineKeyboardButton(text='📣 לערוץ העדכונים 📣', url='https://t.me/JewishBots')],
                              [InlineKeyboardButton(text="🗯 לקבוצת התמיכה 🗯", url="https://t.me/JewsSupport")]])

share = [[InlineKeyboardButton(text='לשיתוף זמני השבת 🕯', switch_inline_query='shabat')], [
    InlineKeyboardButton(text='📣 לערוץ העדכונים 📣', url='https://t.me/JewishBots')
]]

start_help = InlineKeyboardMarkup([[
    InlineKeyboardButton('🔶 לתפריט העזרה לחץ כאן 🔶', url='https://t.me/JewsShabatBot?start=help')
]])

start_stats = InlineKeyboardMarkup([[
    InlineKeyboardButton('📊 לסטטיסטיקות לחץ כאן 📊', url='https://t.me/JewsShabatBot?start=stats')
]])


settings = InlineKeyboardMarkup([[InlineKeyboardButton("חזור להגדרות 🔙", callback_data="BaseSettings")]])


@Client.on_inline_query()
async def shabat_share(_, inline: InlineQuery):
    if inline.query.startswith("shabat"):
        await inline.answer(
            results=[
                InlineQueryResultArticle(
                    title="זמני כניסת השבת",
                    input_message_content=InputTextMessageContent(zmanim),
                    description="לחץ כאן לשיתוף זמני השבת!",
                    thumb_url="https://telegra.ph/file/284d7ceb4b4292dede7ad.jpg",
                    reply_markup=InlineKeyboardMarkup(share))],
            cache_time=5)
    elif inline.query == "":
        text = "על ידי הוספת הרובוט לקבוצה (עם הרשאות מתאימות כמובן...) הקבוצה תסגר אוטומאטית לפני השבת ותפתח מיד עם " \
               "צאת השבת!"
        answers = [InlineQueryResultArticle(
            title="רובוט שומר שבת! נוצר על ידי @JewishBots",
            description="לחץ כאן לעזרה",
            thumb_url="https://telegra.ph/file/284d7ceb4b4292dede7ad.jpg",
            input_message_content=InputTextMessageContent(
                message_text=text
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("לשיתוף זמני כניסת השבת 🕯", switch_inline_query="shabat")],
                [InlineKeyboardButton(text="🗯 לקבוצת התמיכה 🗯", url="https://t.me/JewsSupport"),
                 InlineKeyboardButton(text='📣 לערוץ העדכונים 📣', url='https://t.me/JewishBots')]
            ])
        )]
        await inline.answer(answers, cache_time=5)
