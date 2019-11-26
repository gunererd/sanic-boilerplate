from sanic import Sanic


def create_app(settings):
    app = Sanic(__name__)
    app.settings = settings

    from .services import init_services
    app.register_listener(init_services, 'before_server_start')

    from .apis import init_apis
    init_apis(app, settings)

    return app
