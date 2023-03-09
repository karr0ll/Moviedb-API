from flask import request
from flask_restx import Resource, Namespace

from utils.container import favorite_service
from utils.decorator import auth_required
from utils.logger import logger

favorites_ns = Namespace("favorites", "Эндпойнты работы с избранными фильмами пользователей")


@favorites_ns.route("/movies/<int:mid>")
class FavoritesViews(Resource):
    @favorites_ns.doc(responses={
        201: "Created",
        400: "Empty auth header",
        401: "Authorization required",
    }, params={
        "mid": "id фильма"
    }, security='JWT')
    @auth_required
    def post(self, mid):
        """
        Добавление фильма в favorites пользователя.
        Добавляет в таблицу favorites фильм по его id и
        связывает его с id пользователя,
        полученным из заголовка
        """
        user_data = request.headers(["Authorization"], None)
        if None in user_data:
            logger.info(f"Заголовок запроса POST favorites/movies/{mid} не содержит необходимые данные, 400")
            return "", 400
        try:
            favorites = favorite_service.add_one(mid, user_data)
            logger.info(f"Запрос POST favorites/movies/{mid}, 201")
            return "", 201, {"location": f'/favorites/{favorites.id}'}
        except Exception as e:
            logger.info(f" {e} Запрос POST favorites/movies/{mid} не прошел аутентификацию, 401")
            return str(e), 401

    @favorites_ns.doc(responses={
        204: "Deleted",
    }, security='JWT')
    @auth_required
    def delete(self, mid):
        """
        Удаление фильма из favorites пользователя.
        Удаляет из таблицы favorites фильм по связке id фильма и
        id пользователя, полученным из заголовка
        """
        user_data = request.headers["Authorization"]
        favorite_service.delete_one(mid, user_data)
        logger.info(f"Запрос DELETE favorites/movies/{mid}, 204")
        return "", 204


