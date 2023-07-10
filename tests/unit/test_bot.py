import tests.unit.test_env_utils
import bot
import numpy as np

from config import messages
from unittest import TestCase
from unittest.mock import patch, ANY, call
from bot import start, get_text_messages, search_photo
from telebot.types import Message, User, Chat, PhotoSize


class BotTestCase(TestCase):
    def setUp(self) -> None:
        self.bot_patcher = patch.object(bot, 'bot')
        self.repository_patcher = patch.object(bot, 'repository')
        self.image_service_patcher = patch.object(bot, 'image_service')
        self.storage_service_patcher = patch.object(bot, 'storage_service')
        self.face_index_patcher = patch('bot.FaceIndex')

        self.mock_bot = self.bot_patcher.start()
        self.mock_repository = self.repository_patcher.start()
        self.mock_image_service = self.image_service_patcher.start()
        self.mock_storage_service = self.storage_service_patcher.start()
        self.mock_face_index = self.face_index_patcher.start()

        self.mock_repository.get_available_albums.return_value = ['album1', 'album2']
        self.mock_bot.download_file.return_value = bytes()

        self.user_id = 1
        self.test_message = Message(
            from_user=User(id=self.user_id, username='some_user', is_bot=False, first_name='User'),
            content_type='text', message_id='10', date='2022-02-03',
            chat=Chat(id=1, type='private'), options='', json_string='')
        self.test_message.photo = [PhotoSize(file_id='1', height=100, width=100, file_unique_id='222')]

    def test_start(self):
        start(self.test_message)
        self.mock_bot.send_message.assert_called()

    def test_list_albums(self):
        self.test_message.text = messages['list_albums']
        get_text_messages(self.test_message)
        self.mock_bot.send_message.assert_called_with(self.test_message.from_user.id, messages['choose_album'],
                                                      reply_markup=ANY)

    def test_get_text_messages_chose_album(self):
        self.test_message.text = 'album1'
        get_text_messages(self.test_message)
        self.mock_bot.send_message.assert_called_with(self.test_message.from_user.id, messages['send_photo'])
        self.mock_repository.submit_chosen_album.assert_called_with(self.test_message.from_user.username, 'album1')

    def test_get_text_messages_invalid_input(self):
        self.test_message.text = 'fadfadfasdfasdfa'
        get_text_messages(self.test_message)
        self.mock_bot.send_message.assert_called_with(self.test_message.from_user.id, messages['incorrect_input'])

    def test_search_photo_without_face(self):
        self.mock_image_service.get_face_embeddings_from_bytes.return_value = np.empty(0)
        search_photo(self.test_message)
        self.mock_bot.send_message.assert_called_with(self.test_message.from_user.id, messages['no_face_on_photo'])

    def test_search_photo_multiple_faces(self):
        self.mock_image_service.get_face_embeddings_from_bytes.return_value = np.zeros((2, 2))
        search_photo(self.test_message)
        self.mock_bot.send_message.assert_called_with(self.test_message.from_user.id, messages['too_many_faces'])

    def test_search_photo_not_found(self):
        self.mock_image_service.get_face_embeddings_from_bytes.return_value = np.zeros((1, 2))
        self.mock_repository.get_chosen_album.return_value = ('index_file.pkl', 'mapping_file.pkl')
        search_photo(self.test_message)
        expected_calls = [call.send_message(self.test_message.from_user.id, messages['wait']),
                          call.send_message(self.test_message.from_user.id, messages['no_photos'])]
        self.mock_bot.send_message.assert_has_calls(expected_calls)

    def test_search_photo_found_results(self):
        self.mock_image_service.get_face_embeddings_from_bytes.return_value = np.zeros((1, 2))
        self.mock_repository.get_chosen_album.return_value = ('index_file.pkl', 'mapping_file.pkl')
        self.mock_storage_service.read_pickle.return_value = {1: 'image_1.png', 2: 'image_2.png', 3: 'image_3.png'}
        self.mock_storage_service.download_as_bytes.return_value = bytes()
        self.mock_face_index().search_face.return_value = [1, 2, 3]
        search_photo(self.test_message)
        expected_calls = [call.send_message(self.test_message.from_user.id, messages['wait']),
                          call.send_media_group(self.test_message.from_user.id, ANY)]
        self.mock_bot.send_message.assert_has_calls(expected_calls)

    def tearDown(self) -> None:
        self.bot_patcher.stop()
        self.repository_patcher.stop()
        self.image_service_patcher.stop()
        self.storage_service_patcher.stop()
