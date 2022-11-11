from typing import List, Optional
from marshmallow import validate, Schema, fields


class ReservationCreation(Schema):
    user_id = fields.Integer()
    car_id = fields.Integer()
    amount_of_hours = fields.Integer()
    reservation_date = fields.DateTime()
    reservation_end = fields.DateTime()

class ReservationInfo(Schema):
    id = fields.Integer()
    user_id = fields.Integer()
    car_id = fields.Integer()
    amount_of_hours = fields.Integer()
    reservation_date = fields.DateTime()
    reservation_end = fields.DateTime()

class ReservationIdShema(Schema):
    orderId = fields.Integer()

