from typing import List

from sqlalchemy import String, Table, ForeignKey, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


user_albums = Table(
    "album_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("album_id", ForeignKey("albums.album_id")),
)


class Album(Base):
    """
    Class representing albums table from the database. Uses sqlalchemy for mapping
    """
    __tablename__ = "albums"

    album_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(500))
    folder_name: Mapped[str] = mapped_column(String(100))
    index_file_name: Mapped[str] = mapped_column(String(100))
    mapping_file_name: Mapped[str] = mapped_column(String(100))


class User(Base):
    """
    Class representing users table from the database. Uses sqlalchemy for mapping
    """
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    albums: Mapped[List[Album]] = relationship(secondary=user_albums)

    chosen_album_id: Mapped[int] = mapped_column(ForeignKey(Album.album_id))
    chosen_album: Mapped[Album] = relationship()
