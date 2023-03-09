from dao.models.director import Director


class DirectorDAO:
    def __init__(self, session):
        self.session = session

    def get_all(self):
        """
        Загружает все записи о режиссерах
        :return directors_list: все записи о режиссерах
        """
        directors_list = self.session.query(Director).all()

        return directors_list

    def get_one(self, did):
        """
        Загружает одну запись о режиссере по его id
        :return director: одна запись о режиссере
        """
        director = self.session.query(Director).get(did)

        return director
