from sqlalchemy import func

from dao.models.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        загружает список всех режиссеров
        """
        directors_list = self.session.query(Director).all()

        return directors_list

    def get_one(self, did):
        """
        загружает данные одного режиссера
        """
        director = self.session.query(Director).get(did)

        return director

    def get_director_by_name(self, data):
        """
        загружает id жанра
        """
        director = self.session.query(Director).filter(Director.name == data)
        return director

    def create(self, director_id, director_name):
        """
        создает нового режиссера
        """
        new_genre = Director(
            id=director_id,
            name=director_name
        )
        self.session.add(new_genre)
        self.session.commit()

    def update(self, director):
        """
        обвновляет данные о фильме по его id
        """
        self.session.add(director)
        self.session.commit()

        return director

    def delete(self, did):
        """
        удаляет фильм по его id
        """
        movie = self.get_one(did)
        self.session.delete(movie)
        self.session.commit()