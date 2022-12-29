import pytest

from unittest.mock import MagicMock

from dao.model.director import Director
from dao.director import DirectorDAO
from service.director import DirectorService
from setup_db import db


@pytest.fixture()
def director_dao():
    director_dao = DirectorDAO(db.session)

    jonh = Director(id=1, name='jonh')
    kate = Director(id=2, name='kate')
    oleg = Director(id=3, name='oleg')

    director_dao.get_one = MagicMock(return_value=jonh)
    director_dao.get_all = MagicMock(return_value=[jonh, kate, oleg])
    director_dao.create = MagicMock(return_value=Director(id=3))
    director_dao.delete = MagicMock(return_value=Director(id=2))
    director_dao.update = MagicMock(return_value=Director(id=1))

    return director_dao

class TestDirectorService:
    @pytest.fixture(autouse=True)
    def director_service(self, director_dao):
        self.director_service = DirectorService(dao=director_dao)

    def test_get_one(self):
        director = self.director_service.get_one(1)
        assert director.id != None
        assert director.name != None

    def test_get_all(self):
        directors = self.director_service.get_all()
        assert len(directors) > 0

    def test_create(self):
        director_d = {
            'id': 25,
            'name': 'Carl Johnson'
        }

        director = self.director_service.create(director_d)
        assert director.id != None

    def test_update(self):
        director_d = {
            'id': 1,
            'name': 'ivan'
        }

        self.director_service.update(director_d)

    def test_delete(self):
        self.director_service.delete(3)
