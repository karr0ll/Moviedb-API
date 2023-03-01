from flask import request
from flask_restx import Resource, Namespace

from container import movie_service
from dao.schemas.movie import movies_schema, movie_schema

movies_ns = Namespace('movies')

@movies_ns.route("/")
class MoviesView(Resource):
    # @auth_required
    def get(self):
        """
        получает все фильмы
        """
        page_number = request.args.get("page")
        status = request.args.get("status")
        try:
            if status == "new" and page_number:
                all_movies = movie_service.get_all_new_movies_by_page(page_number)
                return movies_schema.dump(all_movies), 200

            if page_number:
                all_movies = movie_service.get_all_paginated(page_number)
                return movies_schema.dump(all_movies), 200

            all_movies = movie_service.get_all()
            return movies_schema.dump(all_movies), 200

        except Exception as e:
            return str(e), 404

@movies_ns.route('/<int:mid>')
class MovieView(Resource):
    # @auth_required
    def get(self, mid: int):
        """
        получает один фильм по его id
        """
        try:
            movie = movie_service.get_one(mid)

            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404