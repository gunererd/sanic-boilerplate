import json

from sanic import response


def init_api(app):
    @app.route('/api/v1/healthcheck', methods=['GET'])
    async def healthcheck(request):

        return response.json(
            body={},
            status=200
        )
