import jwt

from dao.favorite import FavoriteDAO
from utils.constants import JWT_SECRET, JWT_ALGORITHM


class FavoriteService:
    def __init__(self, dao: FavoriteDAO):
        self.dao = dao

    def add_one(self, mid, user_data):
        """
        реализует логику получения данных об одном фильме по его id
        """
        token = user_data.split("Bearer ")[-1]
        data_from_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data_from_token.get("email")
        uid = self.dao.get_user_id_by_email(email)
        return self.dao.add_one(mid, uid)

    def delete_one(self, mid, user_data):
        """
        реализует логику получения данных об одном фильме по его id
        """
        token = user_data.split("Bearer ")[-1]
        data_from_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data_from_token.get("email")
        uid = self.dao.get_user_id_by_email(email)
        return self.dao.delete_one(mid, uid)
