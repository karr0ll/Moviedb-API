from configs.config_db import db
from dao.models.director import Director
from dao.models.genre import Genre
from dao.models.movie import Movie
from utils.json_reader import read_json


def create_and_load_data():
    """создает и наполняет БД"""
    with db.session.begin():
        db.drop_all()
        db.create_all()

    data = read_json()
    for movie in data["movies"]:
        m = Movie(
            id=movie["pk"],
            title=movie["title"],
            description=movie["description"],
            trailer=movie["trailer"],
            year=movie["year"],
            rating=movie["rating"],
            genre_id=movie["genre_id"],
            director_id=movie["director_id"]
        )
        db.session.add(m)

    for director in data["directors"]:
        d = Director(
            id=director["pk"],
            name=director["name"]
        )
        db.session.add(d)

    for genre in data["genres"]:
        g = Genre(
            id=genre["pk"],
            name=genre["name"],
        )
        db.session.add(g)

    db.session.commit()
