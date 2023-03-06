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

    def update_user(self, data, uid):
        user = self.session.query(User).filter(User.id == uid).first()
        user.name = data.get("name")
        user.surname = data.get("surname")
        user.favorite_genre = data.get("favorite_genre")
        self.session.add(user)
        self.session.commit()

    def update_password(self, new_password_hashed, email):
        uid = self.get_user_id_by_email(email)
        user = self.session.query(User).filter(User.id == uid).first()
        user.password = new_password_hashed
        self.session.add(user)
        self.session.commit()

    def get_user_id_by_email(self, email):
        uid = self.session.query(User.id).filter(User.email == email)
        print(uid)
        return uid

    def get_current_hashed_password_by_id(self, uid):
        current_password = self.session.query(User.password).filter(User.id == uid).first()

        for password in current_password:
            return password
