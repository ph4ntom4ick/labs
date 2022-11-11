from flask import Blueprint, Flask, request, Response, make_response

from werkzeug.security import check_password_hash, generate_password_hash

from manager import *
from models import Reservation
from schemas.reservation import ReservationCreation, ReservationInfo
import random

from flask import jsonify, request, abort
from marshmallow import ValidationError
import sqlalchemy.exc as sql_exception

API_KEY = 'MY_API_KEY'

app = Blueprint('Mars', __name__)
# app = Flask(__name__)

session = DBManager().session()


@app.route("/reservation", methods=["POST"])
def add_reservation() -> Response:

    request_json = request.get_json()
    try:
        # validate request input
        reservation = ReservationCreation().load(request_json)

        # create database record
        reservation_record = Reservation(
            id=random.randint(1, 10000),
            user_id=reservation.get('user_id'),
            car_id=reservation.get('car_id'),
            amount_of_hours=reservation.get('amount_of_hours'),
            reservation_date=reservation.get('reservation_date'),
            reservation_end=reservation.get('reservation_end'),
        )
        session.add(reservation_record)
        session.commit()

    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)

    respose = make_response({"reservationId": reservation_record.id}, 200)
    return respose


@app.route("/reservation/<reservation_id>", methods=["GET"])
def get_reservation(reservation_id) -> Response:


    reservation_record: Reservation = session.query(Reservation).filter(reservation_id == Reservation.id).first()

    if not reservation_record:
        response = {
            "code": 400,
            "message": "There is no such id in database"
        }
        return make_response(response, 400)

    respose = make_response(reservation_record.as_dict(), 200)
    return respose

@app.route("/reservation/<reservation_id>", methods=["DELETE"])
def delete_reservation(reservation_id) -> Response:

    api_key_header = request.headers.get('api_key')
    if False:
        response = {
            "code": 400,
            "message": "Not allowed. Provide a valid api_key header"
        }
        return make_response(response, 400)

    session.query(Reservation).filter(reservation_id == Reservation.id).delete()
    session.commit()

    respose = make_response({"reservationId": reservation_id}, 200)
    return respose

# if __name__ == '__main__':
#     app.run(port=5001)
