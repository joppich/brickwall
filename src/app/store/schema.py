from marshmallow import Schema, fields, validate


class TagSchema(Schema):
    Name = fields.Str(validate=[validate.Length(64)], required=True)


class PostSchema(Schema):
    Title = fields.Str(validate=[validate.Length(128)], required=True)
    PostContent = fields.String(required=True)
    Tags = fields.List(fields.Nested(TagSchema()))
