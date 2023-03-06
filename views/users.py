from flask import request
from flask_restx import Resource, Namespace

from dao.schemas.user import user_schema
from utils.container import user_service
from utils.decorator import auth_required

users_ns = Namespace("user")


@users_ns.route("/")
class UsersViews(Resource):
    @auth_required
    def get(self):
        """
        Получает данные пользователя из заголовка и
        возвращает данные пользователя из базы
        """
        data = request.headers["Authorization"]
        user_data = user_service.get_one(data)
        return user_schema.dump(user_data), 200

    @auth_required
    def patch(self):
        """
        Получает данные пользователя из заголовка и новые данные пользователя,
        и обновляет данные пользователя в базе
        """
        token_data = request.headers["Authorization"]
        user_data = request.json
        try:
            user_service.update_user(token_data, user_data)
            return "", 201
        except Exception as e:
            return str(e), 401

@users_ns.route("/password/")
class UserViews(Resource):
    @auth_required
    def put(self):
        data = request.headers["Authorization"]
        user_data = request.json
        try:
            user_service.update_password(data, user_data)
            return "", 201
        except Exception as e:
            return str(e), 401
