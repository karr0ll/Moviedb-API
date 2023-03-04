from marshmallow import Schema, fields
class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True)