import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import os
from image_service import ImageService
from gcp_service import GCPStorageService
from face_index import FaceIndex
from repository import Repository

bot = telebot.TeleBot(os.environ['BOT_TOKEN'])
image_service = ImageService()
storage_service = GCPStorageService('epam_photos')
repository = Repository()


@bot.message_handler(commands=['start'])
def start(message):
    if message.from_user.username not in repository.get_registered_users():
        bot.send_message(message.from_user.id, "Sorry, you aren't allowed to use this bot")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("List available albums")
    btn2 = types.KeyboardButton('Load new album for indexing')
    markup.add(btn1, btn2)
    bot.send_message(message.from_user.id, "What you would like to do?", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    albums = repository.get_available_albums(message.from_user.username)
    if message.text == 'List available albums':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)  # создание новых кнопок
        buttons = [types.KeyboardButton(album) for album in albums]
        markup.add(*buttons)
        bot.send_message(message.from_user.id, 'Choose the album', reply_markup=markup)
    elif message.text in albums:
        bot.send_message(message.from_user.id, 'Send me you photo for the search')
        repository.submit_chosen_album(message.from_user.username, message.text)
    else:
        bot.send_message(message.from_user.id, "I can't understand you, please choose something from menu")


@bot.message_handler(content_types=['photo'])
def photo(message):
    index_file_name, mapping_file_name = repository.get_chosen_album(message.from_user.username)
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    face = image_service.get_face_embedding_from_bytes(downloaded_file)
    if len(face) == 0:
        bot.send_message(message.from_user.id, "Please, send another photo. I can't detect your face on this one")
    elif len(face) > 1:
        bot.send_message(message.from_user.id, "Please, send another photo. More than 1 face on this photo.")
    else:
        bot.send_message(message.from_user.id, 'Looking for your photos. Give me a second')
        face_index = FaceIndex(storage_service.read_pickle(f'indexes/{index_file_name}'))
        embedding_map = storage_service.read_pickle(f'indexes/{mapping_file_name}')
        result = face_index.search_face(face)
        if len(result) == 0:
            bot.send_message(message.from_user.id, "Unfortunately I wasn't able to find you in this album :(")
        else:
            bot.send_message(message.from_user.id, 'Here is what I found!')
        image_names = [embedding_map[ph] for ph in result]
        photos = [InputMediaPhoto(storage_service.download_as_bytes(img_name)) for img_name in image_names]
        bot.send_media_group(message.from_user.id, photos)


bot.polling(none_stop=True, interval=0)
