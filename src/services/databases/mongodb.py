from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure

from src.services import services_logger
from src.utils import errors


class MongoDb(object):

    def __init__(self, app):
        settings = app.settings
        self.mongo_client = AsyncIOMotorClient(settings['MONGO_CONNECTION_STRING'])
        self.db = self.mongo_client.get_database(settings['MONGO_DATABASE_NAME'])

    async def find_one(self, collection_name, where, select):
        collection = self.db[collection_name]
        return await collection.find_one(where, select)

    async def find(self, collection_name, where, select, limit, skip, sort):
        collection = self.db[collection_name]
        try:
            if not select:
                select = None

            if not limit or limit > 500:
                limit = 500

            cur = collection.find(where, select)

            if skip:
                cur.skip(int(skip))

            if limit:
                cur.limit(int(limit))

            if sort:
                cur.sort(sort)

            items = await cur.to_list(length=None)

            return items

        except OperationFailure as e:
            if e.code in [2, 4]:
                raise errors.Error(
                    context=e.details,
                    err_msg='Please provide valid query...',
                    err_code='errors.badQuery',
                    status=400
                )

            raise


def init_mongodb(app):
    services_logger.info("Initializing mongodb..")
    app.mongodb = MongoDb(app)

