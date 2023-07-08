import utils
from config import messages
from telebot.types import Message, User, Chat
from unittest import TestCase
from unittest.mock import Mock, patch, call

from utils import registration_required, monitored


class RegistrationRequiredTestCase(TestCase):
    def setUp(self) -> None:
        self.repository_mock = Mock()
        self.bot_mock = Mock()
        self.user_id = 1
        self.test_message = Message(from_user=User(id=self.user_id, username='some_user', is_bot=False, first_name='User'),
                                    content_type='text', message_id='10', date='2022-02-03',
                                    chat=Chat(id=1, type='private'), options='', json_string='')
        self.function = Mock()
        self.registration_decorator_function = registration_required(self.repository_mock, self.bot_mock)

    def test_unauthorized_access(self):
        self.repository_mock.is_user_registered.return_value = False
        decorated_func = self.registration_decorator_function(self.function)
        decorated_func(self.test_message)
        self.function.assert_not_called()
        self.bot_mock.send_message.assert_called_with(self.user_id, messages['no_access'])

    def test_authorized_access(self):
        self.repository_mock.is_user_registered.return_value = True
        decorated_func = self.registration_decorator_function(self.function)
        decorated_func(self.test_message)
        self.function.assert_called_with(self.test_message)
        self.bot_mock.assert_not_called()

    @patch("utils.time")
    @patch.object(utils.logger, 'info', autospec=True)
    def test_monitored(self, mock_logging, mock_time):
        decorated_func = monitored(self.function)
        self.function.__name__ = 'test_function'
        decorated_func(self.test_message)
        self.function.assert_called_with(self.test_message)
        mock_time.perf_counter.assert_has_calls([call(), call()])
        mock_logging.assert_called()

