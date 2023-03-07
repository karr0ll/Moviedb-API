from flask import request
from flask_restx import Resource, Namespace

from utils.container import movie_service
from dao.schemas.movie import movies_schema, movie_schema

movies_ns = Namespace('movies', "Эндпойнты работы с сущностями Movies")


@movies_ns.route("/")
class MoviesView(Resource):
    @movies_ns.doc(responses={
        200: 'Success',
        404: 'Not found'
    })
    def get(self):
        """Поулчение списка со всеми фильмами"""
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
class MoviesView(Resource):
    @movies_ns.doc(responses={
        200: 'Success',
        404: 'Not found'
    }, params={
        "mid": "id фильма"
    })
    def get(self, mid: int):
        """
        Получение списка с одним фильмом по его id
        """
        try:
            movie = movie_service.get_one(mid)

            return movie_schema.dump(movie), 200
        except Exception as e:
            return str(e), 404
