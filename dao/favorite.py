from dao.models.favorite import Favorite


class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def add_one(self, mid, uid):
        """
        Добавляет записи о пользователе в таблицу связей
        :param mid: id фильма
        :param uid: id пользователя
        """
        new_favorite = Favorite(
            movie_id=mid,
            user_id=uid
        )
        self.session.add(new_favorite)
        self.session.commit()
        return new_favorite

    def delete_one(self, mid, uid):
        """
        Удаляет запись о пользователе из таблицы связей
        :param mid: id фильма
        :param uid: id пользователя
        """
        favorite_movie = self.session.query(Favorite).filter(
            Favorite.user_id == uid, Favorite.movie_id == mid
        ).one()
        self.session.delete(favorite_movie)
        self.session.commit()


