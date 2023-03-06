from flask import Flask
from flask_restx import Api

from configs.config import Config
from configs.config_db import db
from utils.create_and_load_data import create_and_load_data
from views.auth import auth_ns
from views.directors import directors_ns
from views.favorites import favorites_ns
from views.genres import genres_ns
from views.movies import movies_ns
from views.users import users_ns


def create_app(config):
    application = Flask(__name__)
    application.config.from_object(config)
    application.app_context().push()

    return application


def configure_app(application):
    db.init_app(application)

    api = Api(application)
    api.add_namespace(directors_ns)
    api.add_namespace(genres_ns)
    api.add_namespace(movies_ns)
    api.add_namespace(users_ns)
    api.add_namespace(auth_ns)
    api.add_namespace(favorites_ns)


app_config = Config()
app = create_app(app_config)
configure_app(app)
create_and_load_data()

if __name__ == '__main__':
    app.run()
