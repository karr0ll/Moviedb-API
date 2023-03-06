from sqlalchemy import desc

from dao.models.favorite import Favorite
from dao.models.movie import Movie
from dao.models.user import User


class FavoriteDAO:
    def __init__(self, session):
        self.session = session

    def get_user_id_by_email(self, email):
        uid = self.session.query(User.id).filter(User.email == email)
        return uid

    def add_one(self, mid, uid):
        new_favorite = Favorite(
            movie_id=mid,
            user_id=uid
        )
        self.session.add(new_favorite)
        self.session.commit()
        return new_favorite

    def delete_one(self, mid, uid):
        favorite_movie = self.session.query(Favorite).filter(
            Favorite.user_id == uid, Favorite.movie_id == mid
        ).one()
        self.session.delete(favorite_movie)
        self.session.commit()


