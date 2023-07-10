import os
import functools
from unittest.mock import patch
import utils


def registration_required_mock(_, __):
    def decorator_registration(func):
        @functools.wraps(func)
        def registration_wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return registration_wrapper

    return decorator_registration


utils.registration_required = registration_required_mock

os_patcher = patch.dict(os.environ, {"BOT_TOKEN": "token", 'INSTANCE_CONNECTION_NAME': 'connection',
                                     'DB_PASS': 'db_pass', 'DB_USER': 'user', 'DB_NAME': 'db'})
os_patcher.start()
