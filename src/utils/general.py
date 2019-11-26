import functools
import hashlib
import json
import logging
import os

from dotenv import load_dotenv
from operator import add

logging.basicConfig(level=logging.INFO)


def evaluate_value(value):
    try:
        return int(value)
    except:
        pass

    try:
        return float(value)
    except:
        pass

    return parse_boolean(value, default=value)


def load_settings_from_environments(dotenv_path=None, verbose=True):
    if dotenv_path:
        load_dotenv(dotenv_path=dotenv_path, override=True)
    else:
        load_dotenv(override=True)

    settings = {}
    for key, value in os.environ.items():
        try:
            value = evaluate_value(value)
        except:
            pass

        value = parse_boolean(value, default=value)
        settings[key] = value

    if verbose:
        logging.info(json.dumps(settings, indent=4))

    return settings


def hash_me(*args):
    hashed_string = hashlib.md5(functools.reduce(add, map(lambda arg: str(arg), args)).encode()).hexdigest()
    return hashed_string


def parse_boolean(input, default=None):
    if type(input) is str:
        if input.lower() in ['true', '1', '1.0']:
            return True

        elif input.lower() in ['false', 'null', '0', '0.0']:
            return False

    else:
        if input in [1, 1.0]:
            return True

        elif input in [0, 0.0, None]:
            return False

    return default


def get_project_root_path():
    return os.path.abspath(os.curdir)


def get_project_data_path():
    return get_project_root_path() + '/data'
