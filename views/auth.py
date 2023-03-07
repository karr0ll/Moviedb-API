from flask import request
from flask_restx import Namespace, Resource, fields

from configs.config_db import db
from utils.container import auth_service
from utils.decorator import auth_required

auth_ns = Namespace("auth", "Эндпойнты работы с авторизацией пользователей")


@auth_ns.route("/register")
class AuthView(Resource):
    @auth_ns.doc(responses={
        201: 'Created',
        401: 'Auth required',
        500: 'Server error'
    })
    @auth_ns.expect(auth_ns.model(
        "User", {
            "email": fields.String,
            "password": fields.String,
            "name": fields.String,
            "surname": fields.String,
            "favorite_genre": fields.String
        })
    )
    def post(self):
        """
        Регистрация пользователя.
        Создает в БД запись с данными пользователя,
        полученными из тела запроса
        """
        data = request.json

        email = data.get("email")
        password = data.get("password")
        name = data.get("name", None)
        surname = data.get("surname", None)
        favorite_genre = data.get("favorite_genre", None)

        if None in [email, password]:
            return "", 400
        try:
            user = auth_service.create(data)
            return "", 201, {"location": f'/users/{user.id}'}
        except Exception as e:
            return str(e), 500


@auth_ns.route("/login")
class AuthView(Resource):
    @auth_ns.doc(responses={
        201: 'Created',
        400: 'Bad request',
    }, security='JWT')
    @auth_required
    def post(self):
        """
        Получение access_token и refresh_token.
        Получает в теле запроса данные пользователя
        и возврщает словарь с access_token и refresh_token
        """
        data = request.json

        email = data.get("email", None)
        received_password = data.get("password", None)

        if None in [email, received_password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, received_password)
        user = auth_service.get_by_email(email)
        return tokens, 201, {"location": f'/users/{user.id}'}

    @auth_ns.doc(responses={
        201: 'Created',
        400: 'Bad request',
    }, security='JWT')
    @auth_required
    def put(self):
        """
        Получениу новых access_token и refresh_token.
        Получает в теле запроса access_token и refresh_token
        и возврщает словарь с новыми access_token и refresh_token
        """

        data = request.json

        access_token = data.get("access_token", None)
        refresh_token = data.get("refresh_token", None)
        if None in [access_token, refresh_token]:
            return "", 400
        tokens = auth_service.approve_tokens(access_token, refresh_token)
        return tokens, 201
