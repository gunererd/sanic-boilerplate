import logging

from src.services.http_client import HttpClient
from src.services.databases.mongodb import MongoDb
from src.services.repository import Repository

logging.basicConfig(level=logging.INFO)
services_logger = logging.getLogger('services')


def init_services(app, loop):
    services_logger.info("initializing services...")

    @app.di.register()
    def settings():
        return app.settings

    @app.di.register()
    def http_client():
        return HttpClient()

    @app.di.register()
    def mongodb(settings):
        return MongoDb(settings)

