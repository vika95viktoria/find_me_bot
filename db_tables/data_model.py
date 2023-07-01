from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Column
from sqlalchemy.orm import mapped_column
from typing import List
from sqlalchemy.orm import relationship


class Base(DeclarativeBase):
    pass


user_albums = Table(
    "album_permissions",
    Base.metadata,
    Column("user_id", ForeignKey("findme.users.user_id")),
    Column("album_id", ForeignKey("findme.albums.album_id")),
    schema='findme'
)


class Album(Base):
    __tablename__ = "albums"
    __table_args__ = {'schema': 'findme'}

    album_id: Mapped[int] = mapped_column(primary_key=True)
    full_name: Mapped[str] = mapped_column(String(500))
    folder_name: Mapped[str] = mapped_column(String(100))
    index_file_name: Mapped[str] = mapped_column(String(100))
    mapping_file_name: Mapped[str] = mapped_column(String(100))

class User(Base):
    __tablename__ = "users"
    __table_args__ = {'schema': 'findme'}

    user_id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    albums: Mapped[List[Album]] = relationship(secondary=user_albums)

    chosen_album_id : Mapped[int] = mapped_column(ForeignKey(Album.album_id))
    chosen_album: Mapped[Album] = relationship()



