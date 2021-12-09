import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from database.database import get_all_chats, db
from pyrogram import Client, types
from pyrogram.errors import PeerIdInvalid, ChatAdminRequired, ChatIdInvalid, ChannelInvalid, \
    ChatNotModified, ChatRestricted, ChatWriteForbidden
import nest_asyncio
from pyromod import listen  # don't delete this!
import config
from plugins.markups import share
from shabat import get_out, get_in
from texts import zmanim
import betterlogging as bl

nest_asyncio.apply()  # solve the loop error

plugins = dict(root="plugins")
app = Client('shabat-bot',
             api_id=config.app_id,
             api_hash=config.app_hash,
             bot_token=config.token,
             plugins=plugins)

bl.basic_colorized_config(level=bl.INFO)
logger = bl.getLogger('shabat-bot')

# Muting some pyrogram loggings
bl.getLogger("pyrogram.syncer").setLevel(bl.WARNING)
bl.getLogger("pyrogram.session").setLevel(bl.WARNING)
bl.getLogger("pyrogram.client").setLevel(bl.WARNING)
bl.getLogger("pyrogram.connection.connection").setLevel(bl.WARNING)
bl.getLogger("apscheduler.scheduler").setLevel(bl.WARNING)


async def get_permissions(group) -> types.ChatPermissions:
    permissions = await db.get_permissions(group)
    return types.ChatPermissions(
        can_send_messages=True,
        can_send_media_messages=permissions['can_send_media_messages'],
        can_send_stickers=permissions['can_send_stickers'],
        can_send_animations=permissions['can_send_animations'],
        can_send_games=permissions['can_send_games'],
        can_use_inline_bots=permissions['can_use_inline_bots'],
        can_add_web_page_previews=permissions['can_add_web_page_previews'],
        can_send_polls=permissions['can_send_polls']
    )


async def close():
    permissions = types.ChatPermissions(can_send_messages=False)
    for group in await get_all_chats():
        await asyncio.sleep(0.1)
        photo = await db.get_photo_in(group)
        caption = await db.get_shabat_text(group)
        notifications = await db.get_notifications(group)

        try:
            if notifications is False:
                await app.set_chat_permissions(group, permissions)
                continue
            if not photo:
                await app.send_message(group, caption)
                await app.set_chat_permissions(group, permissions)
            else:
                await app.send_photo(group, photo, caption)
                await app.set_chat_permissions(group, permissions)
        except ChatNotModified:
            continue
        except PeerIdInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChatAdminRequired:
            await app.send_message(group,
                                   "**נראה ששכחתם להביא לי הרשאות מתאימות... אני לא יכול לסגור את הקבוצה הזאת!**")
            continue
        except ChatIdInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChannelInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChatRestricted:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChatWriteForbidden:
            await db.delete_chat(group)
            await app.leave_chat(group)
        except Exception as err:
            logger.warning(f'Chat {group} has been removed from db due {err}')
            await app.send_message(config.log_channel, f'Error in group {group}\n\n {str(err)}')
            continue


async def allow():
    for group in await get_all_chats():
        await asyncio.sleep(0.1)
        permissions = await get_permissions(group)
        photo = await db.get_photo_out(group)
        caption = await db.get_week_text(group)
        notifications = await db.get_notifications(group)
        try:
            if notifications is False:
                await app.set_chat_permissions(group, permissions=permissions)
                continue
            else:
                if not photo:
                    await app.send_message(group, caption)
                    await app.set_chat_permissions(group, permissions=permissions)
                else:
                    await app.send_photo(group, str(photo), caption=caption)
                    await app.set_chat_permissions(group, permissions=permissions)
        except PeerIdInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChatAdminRequired:
            await app.send_message(group,
                                   "**נראה ששכחתם להביא לי הרשאות מתאימות... אני לא יכול לפתוח את הקבוצה הזאת!**")
            continue
        except ChatIdInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChannelInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChatNotModified:
            continue
        except ChatRestricted:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except Exception as err:
            logger.warning(f'Chat {group} has been removed from db due {err}')
            await app.send_message(config.log_channel, f'Error in group {group}\n\n {str(err)}')
            continue


async def shabat_times():
    for group in await get_all_chats():
        try:
            get = await db.get_send_notf(group)
            if get is False:
                continue
        except Exception as err:
            logger.exception(err)
        await asyncio.sleep(0.05)
        try:
            await app.send_message(group, zmanim, reply_markup=types.InlineKeyboardMarkup(share))
            logger.info(f'shabat times sent successfully to: {group}')
        except PeerIdInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except ChannelInvalid:
            await db.delete_chat(group)
            logger.warning(f'Chat {group} has been removed from DB')
            continue
        except Exception as err:
            logger.exception(f'cant send times to  {group} due {err}')
            await app.send_message(config.log_channel, f'Error in group {group}\n\n {str(err)}')
            continue


# split the hours and minutes:
hour_in, min_in = get_in().split(':')
hour_out, min_out = get_out().split(':')

scheduler = AsyncIOScheduler()
# close the group at shabbat
trigger_in = CronTrigger(day_of_week='fri', hour=hour_in, minute=min_in, timezone='Asia/Jerusalem')
# open the group at motzay shabbat
trigger_out = CronTrigger(day_of_week='sat', hour=hour_out, minute=min_out, timezone='Asia/Jerusalem')
# send the shabbat times for group at fri at 13:30
trigger_fri = CronTrigger(day_of_week='fri', hour=13, minute=30, timezone='Asia/Jerusalem')

scheduler.add_job(close, trigger_in)
scheduler.add_job(allow, trigger_out)
scheduler.add_job(shabat_times, trigger_fri)


async def main():
    await app.start()
    logger.info(f'Bot {config.bot_username} Started!')
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        await app.stop()
        scheduler.shutdown()
    except Exception as e:
        logger.exception(e)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(main())
