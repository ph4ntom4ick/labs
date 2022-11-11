from typing import List, Optional
from marshmallow import validate, Schema, fields


class CarCreation(Schema):
    seat_count = fields.Integer(validate=validate.Range(min=1, max=60))
    reservation_price = fields.Integer(
        validate=[validate.Range(min=0, min_inclusive=True, error="Car price should be >= 0.")]
    )

class CarInfo(Schema):
    id = fields.Int()
    seat_count = fields.Integer(validate=validate.Range(min=1, max=60))
    reservation_price = fields.Integer(
        validate=[validate.Range(min=0, min_inclusive=True, error="Car price should be >= 0.")]
    )

class CarIdShema(Schema):
    carId = fields.Int()