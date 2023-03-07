import base64
import hashlib
import hmac

import jwt
from flask import abort

from dao.user import UserDAO
from utils.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS, JWT_SECRET, JWT_ALGORITHM


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def update_user(self, token_data, user_data):
        """
        Реализует логику обновления данных пользователя в БД
        :token_data: данные пользователя из токена, получаемые через заголовок Authorization
        :user_data: данные из json, получаемые в body запроса
        :return: обновление записи о пользователе в БД
        """
        email = self.get_user_email_from_token(token_data)
        uid = self.dao.get_user_id_by_email(email)
        return self.dao.update_user(user_data, uid)

    def update_password(self, token_data, user_data):
        """
        Реализует логику обновления пароля пользователя в БД
        :token_data: токена, получаемый через заголовок Authorization
        :user_data: данные из json, получаемые в body запроса
        :return: bool
        """

        email = self.get_user_email_from_token(token_data)
        uid = self.dao.get_user_id_by_email(email)
        print(uid)
        db_password_hashed = self.dao.get_current_hashed_password_by_id(uid)
        received_password = user_data["password_1"]
        new_password = user_data["password_2"]

        if self.compare_passwords(db_password_hashed, received_password):
            new_password_hashed = self.generate_hashed_password(new_password)
            return self.dao.update_password(new_password_hashed, email)

        if not self.compare_passwords(db_password_hashed, received_password):
            raise abort(400)

    def get_user_email_from_token(self, data):
        """
        Реализует логику получения email пользователя из токена
        :param data: токен, получаемый через заголовок Authorization
        :return email: email пользователя
        """
        token_data = data.split("Bearer ")[-1]
        data_from_token = jwt.decode(token_data, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data_from_token.get("email")

        return email

    def get_one(self, data):
        """
        Реализует логику получения данных пользователя из базы
        :param data: токен, получаемый через заголовок Authorization
        :return data: данные пользователя
        """
        email = self.get_user_email_from_token(data)
        uid = self.dao.get_user_id_by_email(email)
        data = self.dao.get_one(uid)

        return data

    def generate_hashed_password(self, password):
        """
        Реализует логику хеширования открытого пароля пользователя
        :param password: пароль пользователя, получаемый в теле запроса
        :return: хешированный пароль
        """
        hash_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_pass)

    def compare_passwords(self, db_password_hashed, received_password):
        """
        реализует логику проверки двух паролей - текущего пароля в БД
        и полученого в запросе
        :param db_password_hashed: хешированный пароль из БД
        :param received_password: хешированный пароль из тела запроса
        :return: bool
        """
        hash_pass = self.generate_hashed_password(received_password)
        return hmac.compare_digest(db_password_hashed, hash_pass)
