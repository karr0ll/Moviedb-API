from flask import request
from flask_restx import Resource, Namespace, fields

from dao.schemas.user import user_schema
from utils.container import user_service
from utils.decorator import auth_required


users_ns = Namespace("user", "Эндпойнты работы с данными пользователей")


@users_ns.route("/")
class UsersViews(Resource):
    @users_ns.doc(responses={
        200: 'Success',
        401: 'Auth required'
    }, security='JWT')
    @auth_required
    def get(self):
        """
        Получение данных о пользователе.
        Получает данные пользователя из токена, передаваемого в заголовке
        и возвращает данные пользователя из базы
        """
        try:
            data = request.headers["Authorization"]
            user_data = user_service.get_one(data)
            return user_schema.dump(user_data), 200
        except Exception as e:
            return str(e), 401


    @users_ns.doc(responses={
        201: 'Created',
        401: 'Auth required'
    }, security='JWT')
    @users_ns.expect(users_ns.model(
        "User", {
            "name": fields.String,
            "surname": fields.String,
            "favorite_genre": fields.String
        })
    )
    @auth_required
    def patch(self):
        """
        Обновление данных пользователя в базе
        Получает данные пользователя из заголовка и
        новые данные пользователя из тела запроса,
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
    @users_ns.doc(responses={
        201: 'Created',
        401: 'Auth required'
    }, security='JWT')
    @users_ns.expect(users_ns.model(
        "User", {
            "password_1": fields.String,
            "password_2": fields.String
        })
    )
    @auth_required
    def put(self):
        """
        Обновление пароля пользователя.
        Получает данные пользователя из заголовка и
        новые данные пользователя из тела запроса,
        и обновляет пароль пользователя в базе
        """
        data = request.headers["Authorization"]
        user_data = request.json
        try:
            user_service.update_password(data, user_data)
            return "", 201
        except Exception as e:
            return str(e), 401
