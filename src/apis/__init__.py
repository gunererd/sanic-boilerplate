def init_apis(app, settings):

    from .healthcheck import init_api
    init_api(app)
