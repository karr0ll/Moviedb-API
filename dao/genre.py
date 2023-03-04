from dao.models.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        загружает список всех жанров
        """
        genres_list = self.session.query(Genre).all()
        return genres_list

    def get_one(self, gid):
        """
        загружает данные одного жанра
        """
        genre = self.session.query(Genre).get(gid)
        return genre

    def get_genre_by_name(self, data):
        """
        загружает жанр для дальнейшего получения его id
        """
        genre = self.session.query(Genre).filter(Genre.name == data)
        print(genre)
        return genre


    def create(self, genre_id, genre_name):
        """
        создает новый жанр
        """
        new_genre = Genre(
            id=genre_id,
            name=genre_name
        )
        self.session.add(new_genre)
        self.session.commit()

    def update(self, genre):
        """
        обвновляет данные о фильме по его id
        """
        self.session.add(genre)
        self.session.commit()

        return genre

    def delete(self, gid):
        """
        удаляет фильм по его id
        """
        movie = self.get_one(gid)
        self.session.delete(movie)
        self.session.commit()
