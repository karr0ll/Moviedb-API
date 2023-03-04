from sqlalchemy import desc

from dao.models.movie import Movie


class MovieDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        загружает список всех фильмо
        """
        movies_list = self.session.query(Movie).all()
        return movies_list

    def get_one(self, mid):
        """
        загружает один фильм по его id
        """
        movie = self.session.query(Movie).get(mid)
        return movie

    def get_all_by_director(self, director):
        """
        загружает один фильм по фильтру director
        """
        movie = self.session.query(Movie).filter(Movie.director_id == director)
        return movie

    def get_all_by_date_added(self):
        """
        загружает один фильм по фильтру director
        """
        movie = self.session.query(Movie).order_by(desc(Movie.id))
        return movie

    def get_all_by_genre(self, genre):
        """
        загружает один фильм по фильтру genre
        """
        movie = self.session.query(Movie).filter(Movie.genre_id == genre)
        return movie

    def get_all_by_year(self, year):
        """
        загружает один фильм по фильтру year
        """
        movie = self.session.query(Movie).filter(Movie.year == year)
        return movie