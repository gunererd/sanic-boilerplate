import json

import pytest


class TestHealtcheck(object):


    @pytest.fixture(scope='class')
    def url(self):
        return f'/api/v1/healthcheck'

    async def test_get_must_return_200(self, test_cli, url):
        response = await test_cli.get(url)
        assert response.status == 200


