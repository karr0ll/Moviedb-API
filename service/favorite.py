import jwt

from dao.favorite import FavoriteDAO
from dao.user import UserDAO
from utils.constants import JWT_SECRET, JWT_ALGORITHM


class FavoriteService:
    def __init__(self, dao: FavoriteDAO, user_dao: UserDAO):
        self.dao = dao
        self.user_dao = user_dao

    def add_one(self, mid, user_data):
        """
        реализует логику добавления id фильма и пользователя в таблицу favorites
        :param mid: id фильма, получаемый из параметра route
        :param user_data: данные, получаемые из headers["Authorization"]
        """
        token = user_data.split("Bearer ")[-1]
        data_from_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data_from_token.get("email")
        uid = self.user_dao.get_user_id_by_email(email)
        return self.dao.add_one(mid, uid)

    def delete_one(self, mid, user_data):
        """
        реализует логику удаления данных об одном фильме по его id
        """
        token = user_data.split("Bearer ")[-1]
        data_from_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data_from_token.get("email")
        uid = self.user_dao.get_user_id_by_email(email)
        return self.dao.delete_one(mid, uid)
