from sqlalchemy import desc

from dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        Загружает все записи о фильмах
        :return movies_list: все записи о фильмах
        """
        movies_list = self.session.query(Movie).all()
        return movies_list

    def get_one(self, mid):
        """
        Загружает одну запись о фильме по его id
        :return movies: одна запись о фильме
        """
        movie = self.session.query(Movie).get(mid)
        return movie


    def get_all_by_date_added(self):
        """
        Загружает все записи о фильмах, отсортированные по id
        :return movies_list: все записи о фильмах
        """
        movie = self.session.query(Movie).order_by(desc(Movie.id))
        return movie