import os
import sqlite3

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from config import PROJECT_ROOT, TESTS_FOLDER
from services.repository import Repository

DATABASE_FILENAME = 'test_database.db'
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DATABASE_FILENAME}"


def init_database():
    if os.path.isfile(DATABASE_FILENAME):
        os.remove(DATABASE_FILENAME)
    with sqlite3.connect(DATABASE_FILENAME) as db:
        with open(PROJECT_ROOT / 'data/db_schema.sql') as f:
            db.cursor().executescript(f.read())
        with open(TESTS_FOLDER / 'data/test_data.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


init_database()
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
repository = Repository(engine)


@pytest.mark.parametrize("username,is_registered", [("user_1", True), ("user_2", True), ("user_10", False),
                                                    ("user_100", False)])
def test_is_user_registered(username, is_registered):
    assert repository.is_user_registered(username) == is_registered


@pytest.mark.parametrize("username,albums", [("user_1", ['album_1', 'album_2', 'album_3', 'album_4']),
                                             ("user_2", ['album_1', 'album_2', 'album_3']),
                                             ("user_3", ['album_2', 'album_4'])
                                             ])
def test_get_available_albums(username, albums):
    assert repository.get_available_albums(username) == albums


@pytest.mark.parametrize("username,index_file,mapping_file", [("user_1", 'index_3.pkl', 'mapping_3.pkl'),
                                                              ("user_2", 'index_1.pkl', 'mapping_1.pkl')
                                                              ])
def test_chosen_album(username, index_file, mapping_file):
    assert repository.get_chosen_album(username) == (index_file, mapping_file)


@pytest.mark.parametrize("username,album_name,index_file,mapping_file",
                         [("user_3", 'album_4', 'index_4.pkl', 'mapping_4.pkl'),
                          ("user_5", 'album_1', 'index_1.pkl', 'mapping_1.pkl')])
def test_submit_chosen_album_for_the_first_time(username, album_name, index_file, mapping_file):
    repository.submit_chosen_album(username, album_name)
    assert repository.get_chosen_album(username) == (index_file, mapping_file)


@pytest.mark.parametrize("username,album_name,index_file,mapping_file",
                         [("user_1", 'album_4', 'index_4.pkl', 'mapping_4.pkl'),
                          ("user_2", 'album_3', 'index_3.pkl', 'mapping_3.pkl')])
def test_change_chosen_album(username, album_name, index_file, mapping_file):
    assert repository.get_chosen_album(username) != (index_file, mapping_file)
    repository.submit_chosen_album(username, album_name)
    assert repository.get_chosen_album(username) == (index_file, mapping_file)
