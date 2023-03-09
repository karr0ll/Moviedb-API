import logging

from flask import request
from flask_restx import Namespace, Resource, fields

from utils.container import auth_service
from utils.decorator import auth_required
from utils.logger import logger

auth_ns = Namespace("auth", "Эндпойнты работы с авторизацией пользователей")


@auth_ns.route("/register")
class AuthView(Resource):
    @auth_ns.doc(responses={
        201: 'Created',
        400: 'Bad request',
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
            logger.info("Тело запроса POST auth/register не содержит email или пароль,"
                        " 400")
            return "", 400
        try:
            user = auth_service.create(data)
            logger.info("Запрос POST auth/register, 201")
            return "", 201, {"location": f'/users/{user.id}'}
        except Exception as e:
            logger.warning("Ошбика сервера при обработке POST auth/register, 500")
            return str(e), 500


@auth_ns.route("/login")
class AuthView(Resource):
    @auth_ns.doc(responses={
        201: 'Created',
        400: 'Bad request',
    }, security='JWT')
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
            logger.info("Тело запроса POST auth/login не содержит email или пароль, 400")
            return "", 400

        tokens = auth_service.generate_tokens(email, received_password)
        user = auth_service.get_by_email(email)
        logger.info("Запрос POST auth/login, 201")
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
            logger.info("Тело запроса PUT auth/login не содержит email или пароль, 400")
            return "", 400
        tokens = auth_service.approve_tokens(access_token, refresh_token)
        logger.info("Запрос PUT auth/register, 201")
        return tokens, 201
