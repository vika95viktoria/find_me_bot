from sqlalchemy import select
from sqlalchemy.orm import Session
from connection import connect_with_connector
from db_tables.data_model import User, Album

engine = connect_with_connector()
session = Session(engine)


def get_registered_users():
    stmt = select(User.name)
    return [x for x in session.scalars(stmt)]


def get_available_albums(user_name: str):
    stmt = select(User).where(User.name == user_name)
    return [album.full_name for album in session.scalars(stmt).one().albums]


def submit_chosen_album(user_name, album_name):
    get_user_stmt = select(User).where(User.name == user_name)
    get_album_stmt = select(Album).where(Album.full_name == album_name)
    user = session.scalars(get_user_stmt).one()
    album = session.scalars(get_album_stmt).one()
    user.chosen_album = album
    session.commit()


def get_chosen_album(user_name: str):
    stmt = select(User).where(User.name == user_name)
    album = session.scalars(stmt).one().chosen_album
    return album.index_file_name, album.mapping_file_name

