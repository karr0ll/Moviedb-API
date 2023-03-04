from marshmallow import Schema, fields

from dao.schemas.director import DirectorSchema
from dao.schemas.genre import GenreSchema


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre = fields.Pluck(GenreSchema, "name")
    director = fields.Pluck(DirectorSchema, "name")


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)