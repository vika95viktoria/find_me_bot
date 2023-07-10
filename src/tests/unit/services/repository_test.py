from unittest import TestCase
from unittest.mock import patch, call

from db.data_model import User, Album
from services.repository import Repository


class RepositoryTestCase(TestCase):
    def setUp(self) -> None:
        self.db_connector_patcher = patch('services.repository.DbConnector')
        self.mock_db_connector = self.db_connector_patcher.start()
        self.session_patcher = patch('services.repository.Session')
        self.mock_session = self.session_patcher.start()
        self.repository = Repository()
        self.user_with_albums = User(
            user_id=123, name='user', albums=[
                Album(album_id=1, full_name='Album 1'),
                Album(album_id=2, full_name='Album 2'),
                Album(album_id=3, full_name='Album 3')
            ],
            chosen_album=Album(
                album_id=1, full_name='Album 1', index_file_name='album_index', mapping_file_name='album_mapping'
            )
        )
        self.user_without_albums = User(user_id=100, name='user_name', albums=[])

    def test_is_user_registered(self):
        self.mock_session().execute.return_value.scalar.return_value = False
        is_registered = self.repository.is_user_registered('user_name')
        self.assertFalse(is_registered)

    def test_get_available_albums_without_albums(self):
        self.mock_session().scalars.return_value.one.return_value = self.user_without_albums
        result = self.repository.get_available_albums(self.user_without_albums.name)
        self.assertEqual(result, [])

    def test_get_available_albums_with_albums(self):
        self.mock_session().scalars.return_value.one.return_value = self.user_with_albums
        result = self.repository.get_available_albums(self.user_with_albums.name)
        self.assertEqual(result, ['Album 1', 'Album 2', 'Album 3'])

    def test_get_chose_album(self):
        self.mock_session().scalars.return_value.one.return_value = self.user_with_albums
        result = self.repository.get_chosen_album(self.user_with_albums.name)
        self.assertEqual(result, (self.user_with_albums.chosen_album.index_file_name,
                                  self.user_with_albums.chosen_album.mapping_file_name))

    @patch("services.repository.select")
    def test_submit_chosen_album(self, mock_select):
        self.repository.submit_chosen_album('user', 'album')
        self.mock_session().scalars.assert_has_calls([call(mock_select().where()), call().one(),
                                                      call(mock_select().where()), call().one()])
        self.mock_session().commit.assert_called()

    def tearDown(self) -> None:
        self.db_connector_patcher.stop()
        self.session_patcher.stop()
