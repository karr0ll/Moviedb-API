from marshmallow import Schema, fields


class FavoritesSchema(Schema):
    id = fields.Int()
    user_id = fields.Str()
    movie_id = fields.Str()


user_schema = FavoritesSchema()
users_schema = FavoritesSchema(many=True)