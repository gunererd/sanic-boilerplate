import logging

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import OperationFailure, DuplicateKeyError

from src.utils import errors

logger = logging.Logger('MongoDB')


def maybe_object_id(maybe_id):
    if isinstance(maybe_id, ObjectId):
        return maybe_id
    elif not ObjectId.is_valid(maybe_id):
        return maybe_id
    else:
        return ObjectId(maybe_id)


def create_id():
    return ObjectId()


class MongoDb(object):

    def __init__(self, settings):
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

    async def save(self, document, collection_name, force=False):
        collection = self.db[collection_name]

        if "_id" not in document:
            document["_id"] = create_id()
        else:
            document['_id'] = maybe_object_id(document['_id'])
        try:
            if force:
                await collection.replace_one(
                    {'_id': document['_id']},
                    document,
                    upsert=True
                )
            else:
                await collection.insert_one(document)

        except DuplicateKeyError as e:
            raise errors.Error(
                err_code="errors.duplicateKeyError",
                status=409,
                err_msg="There is already existing record in collection<{}>.".format(collection_name),
                context={
                    'collection': collection_name,
                    'error_message': e.details['errmsg']
                }
            )

        return document
