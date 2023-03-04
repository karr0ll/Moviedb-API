from marshmallow import Schema, fields

class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()

director_schema = DirectorSchema()
directors_schema = DirectorSchema(many=True)