from dao.models.user import User


class UserDAO:
    def __init__(self, session):
        self.session = session

    def get_one(self, uid):
        """
        Получает запись из БД об одном пользователе
        :param uid: id пользователя
        :return user_data: данные пользователя
        """
        user_data = self.session.query(
            User.id,
            User.email,
            User.name,
            User.surname,
            User.favorite_genre
        ).filter(User.id == uid).first()
        return user_data

    def update_user(self, data, uid):
        """
        Обновляет запись в БД об одном пользователе
        :param data: данные пользователя из JSON
        :param uid: id пользователя
        """
        user = self.session.query(User).filter(User.id == uid).first()
        user.name = data.get("name")
        user.surname = data.get("surname")
        user.favorite_genre = data.get("favorite_genre")
        self.session.add(user)
        self.session.commit()

    def update_password(self, new_password_hashed, email):
        """
        Обновляет пароль пользователя в БД
        :param new_password_hashed: новый хешированный пароль пользователя
        :param email: email пользователя для поиска id пользователя для обновления
        """
        uid = self.get_user_id_by_email(email)
        user = self.session.query(User).filter(User.id == uid).first()
        user.password = new_password_hashed
        self.session.add(user)
        self.session.commit()

    def get_user_id_by_email(self, email):
        """
        Ищет id пользователя в БД по его email
        :param email: email пользователя для поиска записи пользователя для обновления
        :return uid: id пользователя
        """
        uid = self.session.query(User.id).filter(User.email == email)
        return uid

    def get_current_hashed_password_by_id(self, uid):
        """
        Получает текущий хешированный пароль пользователя по его id
        :param uid: id пользователя
        :return password: хешированный пароль пользователя
        """
        current_password = self.session.query(User.password).filter(User.id == uid).first()

        for password in current_password:
            return password
