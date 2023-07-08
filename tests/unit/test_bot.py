import os

from bot import start, get_text_messages, search_photo, get_photo_from_message, get_photos_from_album
from telebot.types import Message, User, Chat
from unittest import TestCase
from unittest.mock import patch
import bot


class BotTestCase(TestCase):
    def setUp(self) -> None:
        self.bot_patcher = patch('bot.telebot.TeleBot')
        self.image_service_patcher = patch('bot.ImageService')
        self.gcp_service_patcher = patch('bot.GCPStorageService')
        self.repository_patcher = patch('bot.Repository')
        #self.mock_os = patch.object(bot.os.environ, 'get', autospec=True)

        self.mock_bot = self.bot_patcher.start()
        self.mock_image_service = self.image_service_patcher.start()
        self.mock_gcp_service = self.gcp_service_patcher.start()
        self.mock_repository = self.repository_patcher.start()

        self.user_id = 1
        self.test_message = Message(
            from_user=User(id=self.user_id, username='some_user', is_bot=False, first_name='User'),
            content_type='text', message_id='10', date='2022-02-03',
            chat=Chat(id=1, type='private'), options='', json_string='')

    @patch.object(os.environ, 'get', autospec=True)
    def test_start(self, mock_os):
        start(self.test_message)
        self.mock_bot.assert_called()


    def test_get_text_messages(self):
        pass

    def test_search_photo(self):
        pass

    def tearDown(self) -> None:
        self.bot_patcher.stop()
        self.gcp_service_patcher.stop()
        self.repository_patcher.stop()
        self.image_service_patcher.stop()
