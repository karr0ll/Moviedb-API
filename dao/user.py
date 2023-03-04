from sqlalchemy.orm import load_only

from dao.models.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        user_data = self.session.query(
            User.id,
            User.email,
            User.name,
            User.surname,
            User.favorite_genre
        ).filter(User.id == uid).first()

        return user_data

    def update_user(self, user_data):
        uid = user_data.get("id")
        user = self.get_one(uid)
        user.id = uid
        user.email = user_data.get("email")
        user.password = user_data.get("password")
        user.name = user_data.get("name")
        user.surname = user_data.get("surname")
        user.favorite_genre = user_data.get("favorite_genre")
        self.session.add(user)
        self.session.commit()

    def get_current_password_hashed_by_id(self, uid):
        current_password = self.session.query(User.password).filter(User.id == uid).first()

        for password in current_password:
            return password

    def update_password(self, user_data, new_password_hashed):
        uid = user_data.get("id")
        user = self.session.query(User).get(uid)
        user.id = uid
        user.email = user_data.get("email")
        user.password = new_password_hashed
        user.name = user_data.get("name", None)
        user.surname = user_data.get("surname", None)
        user.favorite_genre = user_data.get("favorite_genre", None)
        self.session.add(user)
        self.session.commit()


