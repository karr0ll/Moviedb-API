from configs.config_db import db


class Favorite(db.Model):
    __tablename__ = 'favorites'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"))

