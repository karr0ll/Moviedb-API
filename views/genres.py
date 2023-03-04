from flask import request
from flask_restx import Resource, Namespace

from dao.schemas.genre import genres_schema, genre_schema
from utils.container import genre_service

genres_ns = Namespace('genres')

@genres_ns.route("/")
class GenresView(Resource):
    def get(self):
        """
        получает все жанры
        """
        page_number = request.args.get("page")
        try:
            if page_number:
                all_genres = genre_service.get_all_paginated(page_number)
                return genres_schema.dump(all_genres)
            else:
                all_directors = genre_service.get_all()
                return genres_schema.dump(all_directors)

        except Exception as e:
            return str(e), 404

@genres_ns.route("/<int:gid>")
class GenresView(Resource):
    def get(self, gid: int):
        """
        получает один жанр по его id
        """
        try:
            genre = genre_service.get_one(gid)
            return genre_schema.dump(genre), 200
        except Exception as e:
            return str(e), 404