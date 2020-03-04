import logging

from bson import ObjectId
from cachetools import TTLCache

from src.utils import errors
from src.utils.general import hash_me

logger = logging.getLogger('repository')


def maybe_object_id(maybe_id):
    if isinstance(maybe_id, ObjectId):
        return maybe_id
    elif not ObjectId.is_valid(maybe_id):
        return maybe_id
    else:
        return ObjectId(maybe_id)


class Repository(object):

    def __init__(self, db, collection_name):
        logger.info('Repository {} initializing...'.format(collection_name))

        self.cache_hit_counter = 0
        self.cache = TTLCache(maxsize=1000, ttl=300)
        self.db = db
        self.collection_name = collection_name

    async def find_one_by(self, where=None, select=None, raise_exec=True, _ensure_domain_id=True, hit_cache=True):

        hashed_query = hash_me(str(where), str(select))
        if hit_cache and hashed_query in self.cache:
            self.cache_hit_counter += 1
            return self.cache[hashed_query]

        founded = await self.db.find_one(self.collection_name, where, select)

        if founded:
            self.cache[hashed_query] = founded
            return self.cache[hashed_query]

        if not founded and raise_exec:
            raise errors.Error(
                err_code="errors.resourceNotFound",
                status=404,
                err_msg="Not found any resource in collection <{}> with given query <{}>".format(self.collection_name,
                                                                                                 where),
                context={
                    'collection_name': self.collection_name,
                    'where': where
                }
            )

        return founded

    async def find_by(self, where=None, select=None, limit=None,
                      skip=None, sort=None, hit_cache=True):

        hashed_query = hash_me(str(where), str(select))
        if hit_cache and hashed_query in self.cache:
            self.cache_hit_counter += 1
            return self.cache[hashed_query]

        result = await self.db.find(self.collection_name, where, select, limit, skip, sort)

        if result:
            self.cache[hashed_query] = result
            return self.cache[hashed_query]

        return result

    async def find_one_by_id(self, _id, raise_exec=True, hit_cache=True):

        founded = await self.find_one_by(
            where={
                "_id": maybe_object_id(_id)
            },
            raise_exec=raise_exec,
            hit_cache=hit_cache
        )

        return founded

    async def save(self, resource):
        result = await self.db.save(
            document=resource,
            collection_name=self.collection_name
        )

        return result
