import pytest

from unittest.mock import MagicMock

from dao.model.genre import Genre
from dao.genre import GenreDAO
from service.genre import GenreService
from setup_db import db


@pytest.fixture()
def genre_dao():
    genre_dao = GenreDAO(db.session)

    music = Genre(id=1, name='Music')
    military = Genre(id=2, name='Military')
    sport = Genre(id=3, name='Sport')

    genre_dao.get_one = MagicMock(return_value=music)
    genre_dao.get_all = MagicMock(return_value=[music, military, sport])
    genre_dao.create = MagicMock(return_value=Genre(id=3))
    genre_dao.delete = MagicMock(return_value=Genre(id=2))
    genre_dao.update = MagicMock(return_value=Genre(id=1))

    return genre_dao

class TestGenreService:
    @pytest.fixture(autouse=True)
    def genre_service(self, genre_dao):
        self.genre_service = GenreService(dao=genre_dao)

    def test_get_one(self):
        genre = self.genre_service.get_one(1)
        assert genre.id != None
        assert genre.name != None

    def test_get_all(self):
        genres = self.genre_service.get_all()
        assert len(genres) > 0

    def test_create(self):
        genre_d = {
            'id': 25,
            'name': 'Noir'
        }

        genre = self.genre_service.create(genre_d)
        assert genre.id != None

    def test_update(self):
        genre_d = {
            'id': 1,
            'name': 'Reality_Show'
        }

        self.genre_service.update(genre_d)

    def test_delete(self):
        self.genre_service.delete(3)
