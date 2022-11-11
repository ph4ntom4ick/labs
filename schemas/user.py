from typing import List, Optional
from marshmallow import validate, Schema, fields


class UserCreation(Schema):
    username = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.String()

class User(Schema):
    id = fields.Integer()
    username = fields.String()
    firstName = fields.String()
    lastName = fields.String()
    email = fields.String(validate=validate.Email())
    password = fields.String()

class UserIdShema(Schema):
    userId = fields.Integer()