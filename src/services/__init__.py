import logging

logging.basicConfig(level=logging.INFO)
services_logger = logging.getLogger('services')


def init_services(app, loop):

    services_logger.info("initializing services...")

    from .http_client import init_http_client
    init_http_client(app)

    from .databases import init_databases
    init_databases(app)

    from .repository import init_repositories
    init_repositories(app)



