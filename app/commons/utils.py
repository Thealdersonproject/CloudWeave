"""Utils for general usage purpose."""

import os

from dotenv import load_dotenv

load_dotenv()


def get_env(key: str, default_value: str = "") -> str:
    """Searches for the given key in the environment variables, if not found, retrieves default value.

    :param default_value:
    :param key: The name of the environment variable to retrieve.
    :return: The value of the environment variable if it is set, otherwise the default value.
    """
    return os.getenv(key, default_value)
