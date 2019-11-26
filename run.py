from src.utils.general import load_settings_from_environments
from src import create_app

if __name__ == '__main__':

    settings = load_settings_from_environments(verbose=True)
    app = create_app(settings)

    app.run(
        host=app.settings['HOST'],
        port=app.settings['PORT'],
        access_log=app.settings['ENABLE_ACCESS_LOG']
    )
