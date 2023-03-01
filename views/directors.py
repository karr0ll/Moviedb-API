from flask import request
from flask_restx import Resource, Namespace

from container import director_service
from dao.schemas.director import directors_schema, director_schema

directors_ns = Namespace('directors')

@directors_ns.route("/")
class DirectorsView(Resource):
        # @auth_required
        def get(self):
            """
            получает всех режиссеров
            """
            page_number = request.args.get("page")
            try:
                if page_number:
                    all_directors = director_service.get_all_paginated(page_number)
                    return directors_schema.dump(all_directors)
                else:
                    all_directors = director_service.get_all()
                    return directors_schema.dump(all_directors)


            except Exception as e:
                return str(e), 404

@directors_ns.route("/<int:did>")
class DirectorsView(Resource):
    # @auth_required
    def get(self, did: int):
        """
        получает одного режиссера по его id
        """
        try:
            director = director_service.get_one(did)
            return director_schema.dump(director), 200
        except Exception as e:
            return str(e), 404