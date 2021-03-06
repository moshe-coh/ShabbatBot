from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQuery, \
    InlineQueryResultArticle, InputTextMessageContent
from pyrogram import Client
from texts import zmanim

start = InlineKeyboardMarkup([[InlineKeyboardButton(text='馃摚 诇注专讜抓 讛注讚讻讜谞讬诐 馃摚', url='https://t.me/JewishBots')],
                              [InlineKeyboardButton(text="馃棷 诇拽讘讜爪转 讛转诪讬讻讛 馃棷", url="https://t.me/JewsSupport")]])

share = [[InlineKeyboardButton(text='诇砖讬转讜祝 讝诪谞讬 讛砖讘转 馃暞', switch_inline_query='shabat')], [
    InlineKeyboardButton(text='馃摚 诇注专讜抓 讛注讚讻讜谞讬诐 馃摚', url='https://t.me/JewishBots')
]]

start_help = InlineKeyboardMarkup([[
    InlineKeyboardButton('馃敹 诇转驻专讬讟 讛注讝专讛 诇讞抓 讻讗谉 馃敹', url='https://t.me/JewsShabatBot?start=help')
]])

start_stats = InlineKeyboardMarkup([[
    InlineKeyboardButton('馃搳 诇住讟讟讬住讟讬拽讜转 诇讞抓 讻讗谉 馃搳', url='https://t.me/JewsShabatBot?start=stats')
]])


settings = InlineKeyboardMarkup([[InlineKeyboardButton("讞讝讜专 诇讛讙讚专讜转 馃敊", callback_data="BaseSettings")]])


@Client.on_inline_query()
async def shabat_share(_, inline: InlineQuery):
    if inline.query.startswith("shabat"):
        await inline.answer(
            results=[
                InlineQueryResultArticle(
                    title="讝诪谞讬 讻谞讬住转 讛砖讘转",
                    input_message_content=InputTextMessageContent(zmanim),
                    description="诇讞抓 讻讗谉 诇砖讬转讜祝 讝诪谞讬 讛砖讘转!",
                    thumb_url="https://telegra.ph/file/284d7ceb4b4292dede7ad.jpg",
                    reply_markup=InlineKeyboardMarkup(share))],
            cache_time=5)
    elif inline.query == "":
        text = "注诇 讬讚讬 讛讜住驻转 讛专讜讘讜讟 诇拽讘讜爪讛 (注诐 讛专砖讗讜转 诪转讗讬诪讜转 讻诪讜讘谉...) 讛拽讘讜爪讛 转住讙专 讗讜讟讜诪讗讟讬转 诇驻谞讬 讛砖讘转 讜转驻转讞 诪讬讚 注诐 " \
               "爪讗转 讛砖讘转!"
        answers = [InlineQueryResultArticle(
            title="专讜讘讜讟 砖讜诪专 砖讘转! 谞讜爪专 注诇 讬讚讬 @JewishBots",
            description="诇讞抓 讻讗谉 诇注讝专讛",
            thumb_url="https://telegra.ph/file/284d7ceb4b4292dede7ad.jpg",
            input_message_content=InputTextMessageContent(
                message_text=text
            ),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("诇砖讬转讜祝 讝诪谞讬 讻谞讬住转 讛砖讘转 馃暞", switch_inline_query="shabat")],
                [InlineKeyboardButton(text="馃棷 诇拽讘讜爪转 讛转诪讬讻讛 馃棷", url="https://t.me/JewsSupport"),
                 InlineKeyboardButton(text='馃摚 诇注专讜抓 讛注讚讻讜谞讬诐 馃摚', url='https://t.me/JewishBots')]
            ])
        )]
        await inline.answer(answers, cache_time=5)
