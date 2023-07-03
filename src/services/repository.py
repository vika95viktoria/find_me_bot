from sqlalchemy import select, exists
from sqlalchemy.orm import Session
from db.connector import DbConnector
from db.data_model import User, Album
from typing import List


class Repository:
    def __init__(self):
        self.engine = DbConnector().get_engine()
        self.session = Session(self.engine)

    def is_user_registered(self, user_name) -> bool:
        stmt = select(exists(User).where(User.name == user_name))
        return self.session.execute(stmt).scalar()

    def get_available_albums(self, user_name: str) -> List[str]:
        stmt = select(User).where(User.name == user_name)
        return [album.full_name for album in self.session.scalars(stmt).one().albums]

    def submit_chosen_album(self, user_name, album_name):
        get_user_stmt = select(User).where(User.name == user_name)
        get_album_stmt = select(Album).where(Album.full_name == album_name)
        user = self.session.scalars(get_user_stmt).one()
        album = self.session.scalars(get_album_stmt).one()
        user.chosen_album = album
        self.session.commit()

    def get_chosen_album(self, user_name: str) -> (str, str):
        stmt = select(User).where(User.name == user_name)
        album = self.session.scalars(stmt).one().chosen_album
        return album.index_file_name, album.mapping_file_name