from typing import List

from sqlalchemy import select, exists
from sqlalchemy.engine.base import Engine
from sqlalchemy.orm import Session

from db.connector import DbConnector
from db.data_model import User, Album


class Repository:
    """
    Class representing Data Access Layer using sqlalchemy orm
    """

    def __init__(self, engine: Engine = None):
        if not engine:
            self.engine = DbConnector().get_engine()
        else:
            self.engine = engine
        self.session = Session(self.engine)

    def is_user_registered(self, user_name) -> bool:
        """
        Check if user is present in users table
        :param user_name: telegram username
        :return: indicator whether user exists in users table or not
        """
        stmt = select(exists(User).where(User.name == user_name))
        return self.session.execute(stmt).scalar()

    def get_available_albums(self, user_name: str) -> List[str]:
        """
        Get list of albums user has access to
        :param user_name: telegram username
        :return: list of album names available for this user
        """
        stmt = select(User).where(User.name == user_name)
        return [album.full_name for album in self.session.scalars(stmt).one().albums]

    def submit_chosen_album(self, user_name, album_name):
        """
        Update album currently selected by user
        :param user_name: telegram username
        :param album_name: album name
        """
        get_user_stmt = select(User).where(User.name == user_name)
        get_album_stmt = select(Album).where(Album.full_name == album_name)
        user = self.session.scalars(get_user_stmt).one()
        album = self.session.scalars(get_album_stmt).one()
        user.chosen_album = album
        self.session.commit()

    def get_chosen_album(self, user_name: str) -> (str, str):
        """
        Get chosen album artifacts name

        Get faiss index path and mapping file path in GCP for the album currently selected by user
        :param user_name: telegram username
        :return: tuple with faiss index path and mapping file path
        """
        stmt = select(User).where(User.name == user_name)
        album = self.session.scalars(stmt).one().chosen_album
        return album.index_file_name, album.mapping_file_name
