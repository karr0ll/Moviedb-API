import base64
import hashlib
import hmac

from flask import abort

from dao.user import UserDAO
from utils.constants import PWD_HASH_SALT, PWD_HASH_ITERATIONS


class UserService:
    def __init__(self, dao: UserDAO):
        self.dao = dao

    def get_one(self, uid):
        data = self.dao.get_one(uid)

        return data

    def update_user(self, user_data):
        user_data["password"] = self.generate_hashed_password(user_data["password"])
        return self.dao.update_user(user_data)

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

    def update_password(self, user_data):
        entered_password = user_data["password"]
        db_password_hashed = self.dao.get_current_password_hashed_by_id(user_data["id"])

        if self.compare_passwords(db_password_hashed, entered_password):
            new_password_hashed = self.generate_hashed_password(user_data["new_password"])
            return self.dao.update_password(user_data, new_password_hashed)

        if not self.compare_passwords(db_password_hashed, entered_password):
            raise abort(400)






