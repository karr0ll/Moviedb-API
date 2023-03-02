from flask import request
from flask_restx import Namespace, Resource

from utils.container import auth_service

auth_ns = Namespace("auth")

@auth_ns.route("/register")
class AuthView(Resource):
    def post(self):
        data = request.json

        email = data.get("email", None)
        password = data.get("password", None)
        name = data.get("name", None)
        surname = data.get("surname", None)

        if None in [email, password]:
            return "", 400
        try:
            user = auth_service.create(data)
            return "", 201, {"location": f'/users/{user.id}'}
        except:
            Exception
            return "Такой пользователь уже существует", 500


@auth_ns.route("/login")
class AuthView(Resource):
    def post(self):
        data = request.json

        email = data.get("email", None)
        received_password = data.get("password", None)

        if None in [email, received_password]:
            return "", 400

        tokens = auth_service.generate_tokens(email, received_password)
        return tokens, 200

    def put(self):
        data = request.json

        refresh_token = data.get("refresh_token", None)
        tokens = auth_service.approve_tokens(refresh_token)
        return tokens, 400






