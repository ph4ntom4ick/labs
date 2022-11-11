from flask import Blueprint,Flask, request, Response, make_response
from marshmallow.exceptions import ValidationError
from models import Car
from schemas.car import CarCreation, CarInfo
from default_responses import *
from manager import DBManager
from models import Car
import random
import sqlalchemy.exc as sql_exception

API_KEY = 'MY_API_KEY'

app = Blueprint('Yupiter', __name__)
# app = Flask(__name__)

session = DBManager().session()


@app.route("/car", methods=["POST"])
def add_car() -> Response:

    request_json = request.get_json()
    try:
        # validate request input
        car = CarCreation().load(request_json)
        # create database record
        car_record = Car(
            id=random.randint(1, 10000),
            seat_count=car.get('seat_count'),
            reservation_price=car.get('reservation_price')
        )
        session.add(car_record)
        session.commit()

    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)

    respose = make_response({"carId": car_record.id}, 200)
    return respose

@app.route("/carUpdate/<car_id>", methods=["PUT"])
def update_car(car_id) -> Response:

    request_json = request.get_json()
    car_record = session.query(Car).filter(car_id == Car.id).first()
    if not car_record:
        response = {
            "code": 400,
            "message": "There is no such id in database"
        }
        return make_response(response, 400)

    try:
        # validate request input
        car = CarCreation().load(request_json)
        # create database record
        session.query(Car).filter(car_id == Car.id).update(car)
        session.commit()

    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)

    respose = make_response({"carId": car_id}, 200)
    return respose




@app.route("/car/<car_id>", methods=["GET"])
def get_car(car_id) -> Response:

    car_record: Car = session.query(Car).filter(car_id == Car.id).first()

    if not car_record:
        response = {
            "code": 400,
            "message": "There is no such id in database"
        }
        return make_response(response, 400)

    respose = make_response(car_record.as_dict(), 200)
    return respose

@app.route("/car/<car_id>", methods=["DELETE"])
def delete_car(car_id) -> Response:

    api_key_header = request.headers.get('api_key')
    if False:
        response = {
            "code": 400,
            "message": "Not allowed. Provide a valid api_key header"
        }
        return make_response(response, 400)

    session.query(Car).filter(car_id == Car.id).delete()
    session.commit()

    respose = make_response({"carId": car_id}, 200)
    return respose


#! ne tre maybe
# @app.route("/user/login", methods=["GET"])
# def log_user_in() -> Response:

#     username = request.args.get("username")
#     password = request.args.get("password")

#     response = make_response("Logged in", 200)  # Data, Status Code
#     return response

# @app.route("/user/logout", methods=["GET"])
# def log_user_out() -> Response:

#     response = make_response("Logged out", 200)  # Data, Status Code
#     return response
#!

# @app.route("/user/getbookedcar", methods=["GET"])
# def get_booked_cars() -> Response:
#
#     # bookings = [Order().load(DEFAULT_ORDER), Order().load(DEFAULT_ORDER)]
#     # response = make_response(bookings, 200)  # Data, Status Code
#     # return response
#
# @app.route('/user/{userId}', methods=['DELETE'])
# def delete_user():
#     # session.query(Group).filter(Group.id == group.id).delete()
#     # session.commit()
#     # return jsonify({'Message': 'There is no such group now!'})
#     # userId = User().load(DEFAULT_USER)
#     # response = make_response(f"Successfully deleted {userId}", 200)  # Data, Status Code
#     # return response

# if __name__ == '__main__':
#     app.run(port=5001)
