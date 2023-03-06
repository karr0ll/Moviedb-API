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

    def update_user(self, user_data, data):
        email = self.get_user_email_from_token(user_data)
        uid = self.dao.get_user_id_by_email(email)
        return self.dao.update_user(data, uid)

    def update_password(self, token_data, user_data):
        """
        token_data: данные пользователя из токена, получаемые через заголовок Authorization
        user_data: данные из json, получаемые в body запроса
        """

        email = self.get_user_email_from_token(token_data)
        uid = self.dao.get_user_id_by_email(email)
        print(uid)
        db_password_hashed = self.dao.get_current_hashed_password_by_id(uid)
        entered_password = user_data["password_1"]
        new_password = user_data["password_2"]

        if self.compare_passwords(db_password_hashed, entered_password):
            new_password_hashed = self.generate_hashed_password(new_password)
            return self.dao.update_password(new_password_hashed, email)

        if not self.compare_passwords(db_password_hashed, entered_password):
            raise abort(400)

    def get_user_email_from_token(self, data):
        token_data = data.split("Bearer ")[-1]
        data_from_token = jwt.decode(token_data, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        email = data_from_token.get("email")

        return email

    def get_one(self, data):
        email = self.get_user_email_from_token(data)
        uid = self.dao.get_user_id_by_email(email)
        data = self.dao.get_one(uid)

        return data

    def generate_hashed_password(self, password):
        hash_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_pass)

    def compare_passwords(self, db_password_hashed, entered_password):

        hash_pass = self.generate_hashed_password(entered_password)
        return hmac.compare_digest(db_password_hashed, hash_pass)
