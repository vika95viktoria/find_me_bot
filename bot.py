import telebot
from telebot import types
import numpy as np
import pickle
import cv2
import os
from image_service import ImageService
from face_index import FaceIndex
from google.cloud import storage
from repository import get_registered_users, get_available_albums, submit_chosen_album, get_chosen_album

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
image_service = ImageService()

storage_client = storage.Client()
bucket = storage_client.get_bucket('epam_photos')


def get_mapping(pickle_name: str):
    with open(pickle_name, 'rb') as f:
        return pickle.load(f)


@bot.message_handler(commands=['start'])
def start(message):
    if not message.from_user.username in get_registered_users():
        bot.send_message(message.from_user.id, "Sorry, you aren't allowed to use this bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("List available albums")
    btn2 = types.KeyboardButton('Load new album for indexing')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "What you would like to do?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    albums = get_available_albums(message.from_user.username)
    if message.text == 'List available albums':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        buttons = [types.KeyboardButton(album) for album in albums]
        markup.add(*buttons)
        bot.send_message(message.from_user.id, 'Choose the album', reply_markup=markup)
    elif message.text in albums:
        bot.send_message(message.from_user.id, 'Send me you photo for the search')
        submit_chosen_album(message.from_user.username, message.text)
    else:
        bot.send_message(message.from_user.id, "I can't understand you, please choose something from menu")


@bot.message_handler(content_types=['photo'])
def photo(message):
    index_file_name, mapping_file_name = get_chosen_album(message.from_user.username)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    img_arr = np.asarray(bytearray(downloaded_file), dtype="uint8")
    img_arr = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    face = image_service.get_face_embedding(img_arr)
    if len(face) == 0:
        bot.send_message(message.from_user.id, "Please, send another photo. I can't detect your face on this one")
    elif len(face) > 1:
        bot.send_message(message.from_user.id, "Please, send another photo. More than 1 face on this photo.")
    else:
        bot.send_message(message.from_user.id, 'Looking for your photos. Give me a second')
        with bucket.blob(f'indexes/{index_file_name}').open(mode='rb') as f:
            faiss_ind = pickle.load(f)
            face_index = FaceIndex(faiss_index=faiss_ind)
        with bucket.blob(f'indexes/{mapping_file_name}').open(mode='rb') as f:
            embedding_map = pickle.load(f)
        result = face_index.search_face(face)
        if len(result) == 0:
            bot.send_message(message.from_user.id, "Unfortunately I wasn't able to find you in this album :(")
        else:
            bot.send_message(message.from_user.id, 'Here is what I found!')
        image_names = [embedding_map[ph] for ph in result]
        for img_name in image_names:
            img_content = bucket.blob(img_name).download_as_bytes(storage_client)
            bot.send_photo(message.from_user.id, img_content)


bot.polling(none_stop=True, interval=0)
