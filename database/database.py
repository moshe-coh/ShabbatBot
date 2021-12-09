import datetime
import motor.motor_asyncio
import asyncio
import config


class Database:
    """
    Database configuration:
        # = "id" will be integer. the chat id
        # - "shabat_text" will be string. text will be sent to the group every fri.
        # - "good_week" will be string. text will be sent to the group every tzet shabbbt.
        # - "send_notf" will be bool. if bot will send to the group the shabbat times every fry.
        # - "photo_in" will be string. photo id - will be sent to the group every fri if are set.
        # - "photo_out" will be string. photo id - will be sent to the group every at tzet shabbbt if are set.
        # - "permissions" will be dict. dict with chat permissions to open the group at tzet shabbbt.
    """

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.chats

    def new_chat(self, id):
        return dict(id=id,
                    join_date=datetime.date.today().isoformat(),
                    shabat_text="**שבת שלום לכל חברי הקבוצה! הקבוצה סגורה לשליחת הודעות.**",
                    good_week="**שבוע טוב לכל חברי הקבוצה! הקבוצה פתוחה לכתיבת הודעות.**",
                    send_notf=True,
                    photo_in=None,
                    photo_out=None,
                    notifications=True,
                    permissions=dict(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_stickers=True,
                        can_send_animations=True,
                        can_send_games=True,
                        can_use_inline_bots=True,
                        can_add_web_page_previews=True,
                        can_send_polls=True)
                    )

    async def add_chat(self, id):
        chat = self.new_chat(id)
        await self.col.insert_one(chat)

    async def is_chat_exist(self, id):
        chat = await self.col.find_one({'id': int(id)})
        return True if chat else False

    async def total_chat_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_chats(self):
        all_chats = self.col.find({})
        return all_chats

    async def delete_chat(self, chat_id):
        await self.col.delete_many({'id': int(chat_id)})

    async def request_(self, id):
        chat = await self.col.find_one({'id': int(id)})
        return chat

    async def set_shabat_text(self, id, shabat_text):
        await self.col.update_one({'id': id}, {'$set': {'shabat_text': shabat_text}})

    async def get_shabat_text(self, id):
        chat = await self.request_(id)
        return chat.get('shabat_text', False)

    async def set_notf_on(self, id, send_notf):
        await self.col.update_one({'id': id}, {'$set': {'send_notf': send_notf}})

    async def get_send_notf(self, id):
        chat = await self.request_(id)
        return chat.get('send_notf', False)

    async def set_week_text(self, id, good_week):
        await self.col.update_one({'id': id}, {'$set': {'good_week': good_week}})

    async def get_week_text(self, id):
        chat = await self.request_(id)
        return chat.get('good_week', True)

    async def set_photo_in(self, id, photo_in):
        await self.col.update_one({'id': id}, {'$set': {'photo_in': photo_in}})

    async def get_photo_in(self, id):
        chat = await self.request_(id)
        return chat.get('photo_in', False)

    async def set_photo_out(self, id, photo_out):
        await self.col.update_one({'id': id}, {'$set': {'photo_out': photo_out}})

    async def get_photo_out(self, id):
        chat = await self.request_(id)
        return chat.get('photo_out', False)

    async def set_notifications(self, id, notifications):
        await self.col.update_one({'id': id}, {'$set': {'notifications': notifications}})

    async def get_notifications(self, id):
        chat = await self.request_(id)
        return chat.get('notifications', False)

    async def get_permissions(self, id) -> dict:
        permissions = dict(
            can_send_messages='',
            can_send_media_messages='',
            can_send_stickers='',
            can_send_animations='',
            can_send_games='',
            can_use_inline_bots='',
            can_add_web_page_previews='',
            can_send_polls='')

        query = await self.col.find_one({'id': id})
        return query.get('permissions', permissions)

    # >>> laziness
    async def set_can_send_media_messages(self, id, can_send_media_messages):
        await self.col.update_one({'id': id}, {'$set': {'permissions.can_send_media_messages': can_send_media_messages}})

    async def set_can_send_stickers(self, id, can_send_stickers):
        await self.col.update_one({'id': id}, {'$set': {'permissions.can_send_stickers': can_send_stickers}})

    async def set_can_send_animations(self, id, can_send_animations):
        await self.col.update_one({'id': id}, {'$set': {'permissions.can_send_animations': can_send_animations}})

    async def set_can_send_games(self, id, can_send_games):
        await self.col.update_one({'id': id}, {'$set': {'permissions.can_send_games': can_send_games}})

    async def set_can_use_inline_bots(self, id, can_use_inline_bots):
        await self.col.update_one({'id': id}, {'$set': {'permissions.can_use_inline_bots': can_use_inline_bots}})

    async def set_can_add_web_page_previews(self, id, can_add_web_page_previews):
        await self.col.update_one({'id': id},
                                  {'$set': {'permissions.can_add_web_page_previews': can_add_web_page_previews}})

    async def set_can_send_polls(self, id, can_send_polls):
        await self.col.update_one({'id': id}, {'$set': {'permissions.can_send_polls': can_send_polls}})


db = Database(config.db_url, config.bot_username)


async def get_all_chats() -> list:
    chats = []
    async for chat in await db.get_all_chats():
        a = chat['id']
        chats.append(a)
    return chats
