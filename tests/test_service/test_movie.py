import pytest

from unittest.mock import MagicMock

from dao.model.movie import Movie
from dao.movie import MovieDAO
from service.movie import MovieService
from setup_db import db


@pytest.fixture()
def movie_dao():
    movie_dao = MovieDAO(db.session)

    django_unchained = Movie(id=1,
                             title='Джанго освобожденный',
                             description='Эксцентричный охотник за головами, также известный как Дантист, промышляет отстрелом самых опасных преступников. Работенка пыльная, и без надежного помощника ему не обойтись. Но как найти такого и желательно не очень дорогого? Освобождённый им раб по имени Джанго – прекрасная кандидатура. Правда, у нового помощника свои мотивы – кое с чем надо сперва разобраться.',
                             trailer='https://www.youtube.com/watch?v=2Dty-zwcPv4',
                             year=2012,
                             rating=8.4,
                             genre_id=17,
                             director_id=2)
    burlesque = Movie(id=2,
                      title='Бурлеск',
                      description='Али - молодая амбициозная девушка из маленького городка с чудесным голосом, совсем недавно потеряла своих родителей. Теперь никому не нужная, она отправляется в большой город Лос-Анджелес, где устраивается на работу у Тесс, хозяйки ночного клуба «Бурлеск». За короткое время она находит друзей, поклонников и любовь всей своей жизни. Но может ли сказка длиться вечно? Ведь немало людей завидует этой прекрасной танцовщице...',
                      trailer='https://www.youtube.com/watch?v=sgOhxneHkiE',
                      year=2010,
                      rating=6.4,
                      genre_id=18,
                      director_id=5)
    cross_the_line = Movie(id=3,
                           title='Переступить черту',
                           description='Юность певца Джонни Кэша была омрачена гибелью его брата и пренебрежительным отношением отца. Военную службу будущий певец проходил в Германии. После свадьбы и рождения дочери он выпустил свой первый хит и вскоре отправился в турне по США вместе с Джерри Ли Льюисом, Элвисом Пресли и Джун Картер, о которой он безнадёжно мечтал целых десять лет.',
                           trailer='https://www.youtube.com/watch?v=RnFrrzg1OEQ',
                           year=2005,
                           rating=7.8,
                           genre_id=4,
                           director_id=10)

    movie_dao.get_one = MagicMock(return_value=django_unchained)
    movie_dao.get_all = MagicMock(return_value=[django_unchained, burlesque, cross_the_line])
    movie_dao.create = MagicMock(return_value=Movie(id=3))
    movie_dao.delete = MagicMock(return_value=Movie(id=2))
    movie_dao.update = MagicMock(return_value=Movie(id=1))

    return movie_dao

class TestMovieService:
    @pytest.fixture(autouse=True)
    def movie_service(self, movie_dao):
        self.movie_service = MovieService(dao=movie_dao)

    def test_get_one(self):
        movie = self.movie_service.get_one(1)
        assert movie.id != None
        assert movie.title != None
        assert movie.description != None
        assert movie.trailer != None
        assert movie.year != None
        assert movie.rating != None
        assert movie.genre_id != None
        assert movie.director_id != None

    def test_get_all(self):
        movies = self.movie_service.get_all()
        assert len(movies) > 0

    def test_create(self):
        movie_d = {
            'id': 12,
            'title': 'Монстр в Париже',
            'description': 'Париж. 1910 год. Ужасный монстр, напоминающий гигантское насекомое, нагоняет страх на всю Францию. Застенчивый киномеханик и неутомимый изобретатель начинают охоту на него. В этой погоне они знакомятся со звездой кабаре, сумасшедшим ученым и его умной обезьянкой и, наконец, самим монстром, который оказывается совсем не страшным. Теперь безобидное, как блоха, чудовище ищет у своих новых друзей защиты от вредного начальника городской полиции.',
            'trailer': 'https://www.youtube.com/watch?v=rKsdTuvrF5w',
            'year': 2010,
            'rating': 6.1,
            'genre_id': 16,
            'director_id': 18
        }

        movie = self.movie_service.create(movie_d)
        assert movie.id != None
        assert movie.title != None
        assert movie.description != None
        assert movie.trailer != None
        assert movie.year != None
        assert movie.rating != None
        assert movie.genre_id != None
        assert movie.director_id != None

    def test_update(self):
        movie_d = {
            'id': 25,
            'title': 'Монстр в Париже 2',
            'description': 'Париж. 1950 год. Ужасный монстр, напоминающий гигантское насекомое, нагоняет страх на всю Францию. Застенчивый киномеханик и неутомимый изобретатель начинают охоту на него. В этой погоне они знакомятся со звездой кабаре, сумасшедшим ученым и его умной обезьянкой и, наконец, самим монстром, который оказывается совсем не страшным. Теперь безобидное, как блоха, чудовище ищет у своих новых друзей защиты от вредного начальника городской полиции.',
            'trailer': 'https://www.youtube.com/watch?v=rKsdTuvrF5w',
            'year': 2020,
            'rating': 9.5,
            'genre_id': 11,
            'director_id': 12
        }

        self.movie_service.update(movie_d)

    def test_delete(self):
        self.movie_service.delete(3)
