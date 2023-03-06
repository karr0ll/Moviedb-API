import base64
import calendar
import datetime
import hashlib
import hmac

import jwt
from flask import abort

from dao.auth import AuthDAO
from utils.constants import JWT_SECRET, JWT_ALGORITHM, PWD_HASH_SALT, PWD_HASH_ITERATIONS


class AuthService:
    def __init__(self, dao: AuthDAO):
        self.dao = dao

    def create(self, user_data):
        user_data["password"] = self.generate_hashed_password(user_data["password"])
        return self.dao.create(user_data)

    def generate_hashed_password(self, password):
        hash_pass = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            PWD_HASH_SALT,
            PWD_HASH_ITERATIONS
        )
        return base64.b64encode(hash_pass)

    def get_by_email(self, email):
        return self.dao.get_user_data_by_email(email)

    def compare_passwords(self, password, received_password):
        hash_pass = self.generate_hashed_password(received_password)

        return hmac.compare_digest(password, hash_pass)

    def generate_tokens(self, email, received_password, is_refresh=False):
        user_data = self.dao.get_user_data_by_email(email)

        if user_data is None:
            abort(404)

        if not is_refresh:
            if not self.compare_passwords(user_data.password, received_password):
                abort(400)

        data = {
            "email": user_data.email,
            "password": received_password
        }

        token60min = datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        data["exp"] = calendar.timegm(token60min.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

        days10 = datetime.datetime.utcnow() + datetime.timedelta(days=10)
        data["exp"] = calendar.timegm(days10.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
        }

    def approve_tokens(self, access_token, refresh_token):
        try:
            access_token_data = jwt.decode(jwt=access_token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)
            refresh_token_data = jwt.decode(jwt=refresh_token, key=JWT_SECRET, algorithms=JWT_ALGORITHM)

            email = access_token_data.get("email")
            password = refresh_token_data.get("password")

            user_data = self.dao.get_user_data_by_email(email)

            if user_data is None:
                raise abort(400)

            return self.generate_tokens(email, password, is_refresh=True)

        except:
            abort(403)
