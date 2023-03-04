from flask import request
from flask_restx import Resource, Namespace

from dao.schemas.user import user_schema
from utils.container import user_service
from utils.decorator import auth_required

users_ns = Namespace("user")


@users_ns.route("/<int:uid>")
class UsersViews(Resource):
    @auth_required
    def get(self, uid):
        user_data = user_service.get_one(uid)
        return user_schema.dump(user_data), 200

    @auth_required
    def patch(self, uid):
        user_data = request.json
        user_data["id"] = uid
        try:
            user_service.update_user(user_data)
            return "", 201
        except Exception as e:
            return str(e), 404

@users_ns.route("/password/")
class UserViews(Resource):
    @auth_required
    def put(self):
        data = request.json
        try:
            user_service.update_password(data)
            return "", 201
        except Exception as e:
            return str(e), 404
