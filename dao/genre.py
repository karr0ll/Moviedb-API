from dao.models.genre import Genre


class GenreDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        Загружает все записи о жанрах
        :return genres_list: все записи о жанрах
        """
        genres_list = self.session.query(Genre).all()
        return genres_list

    def get_one(self, gid):
        """
        Загружает одну запись о жанре по его id
        :return genre: одна запись о жанре
        """
        genre = self.session.query(Genre).get(gid)
        return genre
