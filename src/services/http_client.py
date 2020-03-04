import logging

from tornado.httpclient import AsyncHTTPClient

from src.utils import errors
from src.utils.json_helpers import safe_load

logger = logging.getLogger('http_client')


class HttpClient(object):

    def __init__(self):
        self.http_client = AsyncHTTPClient()

    async def fetch(self, url, callback=None, raise_error=True, convert_error=False, **kwargs):
        try:
            response = await self.http_client.fetch(url, raise_error=raise_error, **kwargs)

            if response.code >= 400 and convert_error:
                err = safe_load(response)
                raise errors.Error(
                    err_msg='Remote error occured while fetching<{}>'.format(url),
                    err_code='errors.remoteError',
                    context={
                        'remote_error': err
                    },
                    status=500
                )
            return safe_load(response)

        except Exception as e:
            logger.exception("Exception occured while fetchin url<{}>".format(url))
            raise e


def init_http_client(app):
    app.http_client = HttpClient()
