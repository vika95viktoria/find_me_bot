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
    """
    Parse function args and get user details from it

    Take first argument of a function which is expected to be :class:`telebot.types.Message` object and get username and
    id from it
    :param args: arguments of the function
    :return: tuple with username and user_id inside
    """
    message = args[0]
    return message.from_user.username, message.from_user.id


def registration_required(repository: Repository, bot: TeleBot):
    """
    Check if user is authorized to use the bot
    As a parameter to the decorator function, it passes :class:`services.repository.Repository` object
    and :class:`telebot.TeleBot` object.

    Search for the user in `users` table in the database to determine if user can access bot functionality. In case of
    unregistered user send error message using bot api and log the access attempt. Otherwise proceeds with the message
    handling function

    :param repository: DAO providing interface for database communication
    :param bot: telegram bot interface allowing to send messages back to user
    :return: decorated function
    """
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
    """
    Measure time and log info about function invocation

    Add log entry with data about elapsed time for function invocation and user initiated the function execution
    :param func: function to be monitored
    :return: decorated function
    """
    @functools.wraps(func)
    def decorator_monitored(*args, **kwargs):
        username, _ = get_user_from_args(args)
        func_start = time.perf_counter()
        value = func(*args, **kwargs)
        func_end = time.perf_counter()
        logger.info(f'Function {func.__name__} executed by {username} in {func_end - func_start} seconds')
        return value

    return decorator_monitored
