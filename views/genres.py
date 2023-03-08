from flask import request
from flask_restx import Resource, Namespace

from dao.schemas.genre import genres_schema, genre_schema
from utils.container import genre_service
from utils.logger import logger

genres_ns = Namespace('genres', "Эндпойнты работы с сущностями Genres")


@genres_ns.route("/")
class GenresView(Resource):
    @genres_ns.doc(responses={
        200: 'Success',
        404: 'Not found'
    })
    def get(self):
        """
        Получение списка со всеми жанрами
        """
        page_number = request.args.get("page")
        try:
            if page_number:
                all_genres = genre_service.get_all_paginated(page_number)
                logger.info("Запрос GET genres/, 200")
                return genres_schema.dump(all_genres),200
            else:
                all_directors = genre_service.get_all()
                logger.info("Запрос GET genres/, 200")
                return genres_schema.dump(all_directors), 200

        except Exception as e:
            logger.info("Запрос GET genres/, 404. Информация не найдена")
            return str(e), 404


@genres_ns.route("/<int:gid>")
class GenresView(Resource):
    @genres_ns.doc(responses={
        200: 'Success',
        404: 'Not found'
    }, params={
        "gid": "id жанра"
    })
    def get(self, gid: int):
        """
        Получение списка с одним жанром по его id
        """
        try:
            genre = genre_service.get_one(gid)
            logger.info(f"Запрос GET genres/{gid}, 200")
            return genre_schema.dump(genre), 200
        except Exception as e:
            logger.info(f"Запрос GET genres/{gid}, 404. Информация не найдена")
            return str(e), 404
