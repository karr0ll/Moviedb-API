from flask import request
from flask_restx import Resource, Namespace

from dao.schemas.director import directors_schema, director_schema
from utils.container import director_service
from utils.logger import logger

directors_ns = Namespace('directors', "Эндпойнты работы с сущностями Director")


@directors_ns.route("/")
class DirectorsView(Resource):
    @directors_ns.doc(responses={
        200: 'Success',
        404: 'Not found'
    })
    def get(self):
        """
        Получение списка со всеми режиссерами.
        """
        page_number = request.args.get("page")
        try:
            if page_number:
                all_directors = director_service.get_all_paginated(page_number)
                logger.info("Запрос GET directors/, 200")
                return directors_schema.dump(all_directors)
            else:
                all_directors = director_service.get_all()
                logger.info("Запрос GET directors/, 200")
                return directors_schema.dump(all_directors), 200

        except Exception as e:
            logger.info("Запрос GET directors/, 404. Информация не найдена")
            return str(e), 404


@directors_ns.route("/<int:did>")
class DirectorsView(Resource):
    @directors_ns.doc(params={
        "did": "id режиссера"
    }, responses={
        200: 'Success',
        404: 'Not found'
    })
    def get(self, did: int):
        """
        Получение списка с одним режиссером по его id.
        """
        try:
            director = director_service.get_one(did)
            logger.info(f"Запрос GET directors/{did}, 200")
            return director_schema.dump(director), 200
        except Exception as e:
            logger.info(f"Запрос GET directors/{did}, 404. Информация не найдена")
            return str(e), 404
