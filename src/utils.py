import functools
import logging
import sys
import time

from telebot import TeleBot
from services.repository import Repository
from config import messages, LOG_DIR

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_handler = logging.FileHandler(f"{LOG_DIR}/{__name__}.log", mode='w')
logger.addHandler(log_handler)
logger.addHandler(logging.StreamHandler(sys.stdout))


def get_user_from_args(args) -> (str, int):
    message = args[0]
    return message.from_user.username, message.from_user.id


def registration_required(repository: Repository, bot: TeleBot):
    def decorator_registration(func):
        @functools.wraps(func)
        def registration_wrapper(*args, **kwargs):
            username, user_id = get_user_from_args(args)
            if not repository.is_user_registered(username):
                bot.send_message(user_id, messages['no_access'])
                logger.info(f'Unauthorized access from user {username}')
                return
            return func(*args, **kwargs)

        return registration_wrapper

    return decorator_registration


def monitored(func):
    @functools.wraps(func)
    def decorator_monitored(*args, **kwargs):
        username, _ = get_user_from_args(args)
        func_start = time.perf_counter()
        value = func(*args, **kwargs)
        func_end = time.perf_counter()
        logger.info(f'Function {func.__name__} executed by {username} in {func_end - func_start} seconds')
        return value

    return decorator_monitored
