from dao.models.user import User


class AuthDAO:
    def __init__(self, session):
        self.session = session

    def create(self, user_data):
        """
        создает запись с email и хешированным паролем
        :param user_data: email и хешированный пароль пользователя
        :return new_user: созданная запись о пользователе
        """
        new_user = User(**user_data)
        self.session.add(new_user)
        self.session.commit()
        return new_user

    def get_user_data_by_email(self, email):
        """
        запрашивает данные о пользователе в БД по его email
        :param email: email пользователя
        :return user: данные о пользователе из БД
        """
        user = self.session.query(User).filter(User.email == email).first()
        return user
