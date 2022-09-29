from marshmallow import Schema, fields


class ResponseSchema(Schema):
    msg = fields.String(required=True)
