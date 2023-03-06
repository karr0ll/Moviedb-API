from flask import request
from flask_restx import Resource, Namespace

from utils.container import favorite_service
from utils.decorator import auth_required

favorites_ns = Namespace("favorites")


@favorites_ns.route("/movies/<int:mid>")
class FavoritesViews(Resource):
    @auth_required
    def post(self, mid):
        user_data = request.headers["Authorization"]
        try:
            favorites = favorite_service.add_one(mid, user_data)
            return "", 201, {"location": f'/favorites/{favorites.id}'}
        except Exception as e:
            return str(e), 500


    @auth_required
    def delete(self, mid):
        user_data = request.headers["Authorization"]
        favorite_service.delete_one(mid, user_data)
        return "", 204


