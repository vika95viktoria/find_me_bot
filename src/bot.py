import os
from typing import List

import numpy as np
import telebot
from telebot.types import InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton, Message

from config import BUCKET_NAME, INDEXES, messages, BotActions
from index.face_index import FaceIndex
from services.gcp_service import GCPStorageService
from services.image_service import ImageService
from services.repository import Repository
from utils import registration_required, monitored

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
image_service = ImageService()
storage_service = GCPStorageService(BUCKET_NAME)
repository = Repository()


def get_photo_from_message(message: Message) -> bytes:
    """
    Download image file from Telegram message object and store it locally

    :param message: Telegram message object
    :return: image content in bytes
    """
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    return bot.download_file(file_info.file_path)


def get_photos_from_album(user_name: str, face: np.ndarray) -> List[InputMediaPhoto]:
    """
    Search for the photos with user face in chosen album

    Get faiss index file path and mapping object path for the album user has chosen. Read these files from GCP and
    recreate corresponding objects from them using pickle module. Then search for all images with face using faiss index.
    Download all the found photos and create :class:`telebot.types.InputMediaPhoto` objects from them

    :param user_name: telegram username
    :param face: array representing face embedding of the user
    :return: list of :class:`telebot.types.InputMediaPhoto` objects representing found images where face is detected
    """
    index_file_name, mapping_file_name = repository.get_chosen_album(user_name)
    face_index = FaceIndex(storage_service.read_pickle(f'{INDEXES}/{index_file_name}'))
    embedding_map = storage_service.read_pickle(f'{INDEXES}/{mapping_file_name}')
    result = face_index.search_face(face)
    image_names = [embedding_map[photo] for photo in result]
    return [InputMediaPhoto(storage_service.download_as_bytes(img_name)) for img_name in image_names]


@bot.message_handler(commands=['start'])
@registration_required(repository, bot)
@monitored
def start(message: Message):
    """
    Handle initial call from user invocated by '/start' command in Telegram chat

    Render interactive menu with available bot actions for the user and send a message asking to choose the action

    :param message: telegram message
    :return:
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(action.value) for action in BotActions])
    bot.send_message(message.from_user.id, messages['choose_action'], reply_markup=markup)


@bot.message_handler(content_types=['text'])
@registration_required(repository, bot)
@monitored
def get_text_messages(message: Message):
    """
    Handle all text messages from bot users

    Handle message of type text and send the corresponding response for the future interaction with the user. In case
    of unexpected input send error message

    :param message: telegram message
    :return:
    """
    albums = repository.get_available_albums(message.from_user.username)
    if message.text == messages['list_albums']:
        markup = ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[KeyboardButton(album) for album in albums])
        bot.send_message(message.from_user.id, messages['choose_album'], reply_markup=markup)
    elif message.text in albums:
        bot.send_message(message.from_user.id, messages['send_photo'])
        repository.submit_chosen_album(message.from_user.username, message.text)
    else:
        bot.send_message(message.from_user.id, messages['incorrect_input'])


@bot.message_handler(content_types=['photo'])
@registration_required(repository, bot)
@monitored
def search_photo(message: Message):
    """
    Search for all images with the person from the photo

    Download photo from message and get face embedding from it. If there are no face embeddings found on the photo
    or more than one, send the corresponding error message. Otherwise proceed with the search in chosen album. Based on
    the search results either send album with all found photos or text message telling that nothing had been found.

    :param message: telegram message
    :return:
    """
    photo_in_bytes = get_photo_from_message(message)
    face = image_service.get_face_embeddings_from_bytes(photo_in_bytes)
    if len(face) == 0:
        bot.send_message(message.from_user.id, messages['no_face_on_photo'])
    elif len(face) > 1:
        bot.send_message(message.from_user.id, messages['too_many_faces'])
    else:
        bot.send_message(message.from_user.id, messages['wait'])
        found_images = get_photos_from_album(message.from_user.username, face)
        if not found_images:
            bot.send_message(message.from_user.id, messages['no_photos'])
        else:
            bot.send_message(message.from_user.id, messages['photo_found'])
            bot.send_media_group(message.from_user.id, found_images)


if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)
