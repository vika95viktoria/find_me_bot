import telebot
from telebot.types import InputMediaPhoto, ReplyKeyboardMarkup, KeyboardButton, Message
import os
import numpy as np
from config import BUCKET_NAME, INDEXES, messages, BotActions
from recognition.face_index import FaceIndex
from services.image_service import ImageService
from services.gcp_service import GCPStorageService
from services.repository import Repository
from typing import List
from utils import registration_required, monitored


bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
image_service = ImageService()
storage_service = GCPStorageService(BUCKET_NAME)
repository = Repository()


def get_photo_from_message(message: Message) -> bytes:
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    return bot.download_file(file_info.file_path)


def get_photos_from_album(user_name: str, face: np.ndarray) -> List[InputMediaPhoto]:
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
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(*[KeyboardButton(action.value) for action in BotActions])
    bot.send_message(message.from_user.id, messages['choose_action'], reply_markup=markup)


@bot.message_handler(content_types=['text'])
@registration_required(repository, bot)
@monitored
def get_text_messages(message: Message):
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
    photo_in_bytes = get_photo_from_message(message)
    face = image_service.get_face_embedding_from_bytes(photo_in_bytes)
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
    print('Bot is deployed')
    bot.polling(none_stop=True, interval=0)
