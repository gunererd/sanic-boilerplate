import datetime
import decimal
import json

from bson.objectid import ObjectId
from bson.json_util import default


def safe_load(response, object_hook=None):
    if not response.body:
        return {}

    try:
        return json.loads(response.body.decode(), object_hook=object_hook)
    except Exception as e:
        raise e


def parse_date(text):

    formats = [
        '%Y-%m-%d',
        '%Y-%m-%dT%H:%M:%S.%fZ',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%dT%H:%M:%SZ',
        '%m/%d/%Y %I:%M:%S %p'
    ]

    for fmt in formats:
        try:
            return datetime.datetime.strptime(text, fmt)
        except ValueError:
            pass
    raise ValueError('no valid date format found')


def bson_to_json(o):
    if isinstance(o, ObjectId):
        return str(o)
    if isinstance(o, datetime.datetime):
        r = o.isoformat()
        return r + 'Z'
    elif isinstance(o, datetime.date):
        return o.isoformat()
    elif isinstance(o, datetime.time):
        r = o.isoformat()
        if o.microsecond:
            r = r[:12]
        return r
    elif isinstance(o, decimal.Decimal):
        return str(o)
    return default(o)