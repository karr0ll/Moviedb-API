from dao.models.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, user_data):
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_user_data_by_email(self, email):
        user = self.session.query(User).filter(User.email == email).first()
        return user