from dao.auth import AuthDAO
from dao.director import DirectorDAO
from dao.favorite import FavoriteDAO
from dao.genre import GenreDAO
from dao.movie import MovieDAO
from dao.user import UserDAO
from service.auth import AuthService
from service.director import DirectorService
from service.favorite import FavoriteService
from service.genre import GenreService
from service.movie import MovieService
from configs.config_db import db
from service.user import UserService

director_dao = DirectorDAO(db.session)
genre_dao = GenreDAO(db.session)
movie_dao = MovieDAO(db.session)
auth_dao = AuthDAO(db.session)
user_dao = UserDAO(db.session)
favorite_dao = FavoriteDAO(db.session)

director_service = DirectorService(director_dao)
genre_service = GenreService(genre_dao)
movie_service = MovieService(movie_dao)
auth_service = AuthService(auth_dao)
user_service = UserService(user_dao)
favorite_service = FavoriteService(favorite_dao, user_dao)

