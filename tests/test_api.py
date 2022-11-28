from flask import Blueprint, Flask, request, Response, make_response

from werkzeug.security import check_password_hash, generate_password_hash

from labs.manager import *
from labs.models import User, Car, Reservation, Base
from labs.schemas.user import UserCreation
from labs.schemas.car import CarCreation, CarInfo
from labs.schemas.reservation import ReservationCreation, ReservationInfo
import random

from flask import jsonify, abort
from marshmallow import ValidationError
import sqlalchemy.exc as sql_exception
from flask_jwt_extended import JWTManager


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user

import pytest
from labs.main import app

API_KEY = 'MY_API_KEY'

session = DBManager().session()


# schema = UserCreation()
user_2 = {
"username" : "exaple_1",
"firstName": " hitler",
"lastName": "kaput",
"email": "hitlerkaput@gmail.com",
"password": "nazi1"
}

user_3 = {
"username" : "exaple_1",
"password": "nazi1"
}



user_4 = {
"username" : "exaple_1",
"surname":"adolf",
"password": "nazi1"
}

def create_client():
    app.testing = True
    return app.test_client()

client =create_client()


# engine =create_engine('mysql://root:lviv16@127.0.0.1:3306/shos_yak_car_reservation')


# @pytest.fixture(scope='function')
# def wrapper(request):
#     session.close()
#     Base.metadata.drop_all(engine)
#     Base.metadata.create_all(engine)

def test_user():

    session.delete(session.query(User).filter_by(username=user_2["username"]).first())
    resp = client.post('/user/user', json = user_2)
    # print(resp.json)
    assert resp.json['code'], 200
    assert resp.json['message'], 'User added successfully'
    # assert resp.json['userId'] is not None




# def test_login_user():

#     resp = client.post('/user/user', json = user_2)
#     new_user = session.query(User).filter(User.username == user_2["username"]).first()
#     resp = client.get('user/user/login',json = user_3)
#     print(resp.json)
#     assert resp.json['token'] is not None
    # assert resp.status_code == 401
    # assert resp.data ==''
    # assert resp.json==  {
    #     "code": 401,
    #     "message": "Wrong credentials"
    #     }

# def test_update_user():

#     resp = client.put('user/user/492',json = user_4)
#     assert resp.status_code == 200








# def test_bad_user():

#     resp = client.post('/user/user', json = user_4)
#     assert resp.json['code'], 400
#     assert resp.json['message'], 'Server crashed with the following error'










schema = CarCreation()
car_2 = {
"seat_count": 50,
"reservation_price": 1228
}

car_3={
"seat_count": 40,
"reservation_price": 40
}

car_4 = {
"seat_counter": 41
}

def test_add_car():

    # session.delete(session.query(Car).filter_by(seat_count=car_2["seat_count"]).first())
    resp = client.post('/car/car', json = car_2)
    print(resp.json)
    # assert resp.json['code'], 200
    # assert resp.json['message'], 'Car added successfully'
    assert resp.json['carId'] is not None

def test_bad_add_car():

    resp = client.post('/car/car', json = car_4)
    assert resp.json['code'], 400
    assert resp.json['message'], 'bad json'




def test_update_car():

    resp = client.put('car/carUpdate/982',json =car_3)
    print(resp.json)
    # assert resp.json['code'], 200
    assert resp.json['carId'] is not None

def test_bad_update_car():

    resp = client.put('car/carUpdate/100',json =car_3)
    # print(resp.json)
    assert resp.json['code'], 404
    assert resp.json['message'], 'There is no such id in database'


def test_really_bad_update_car():

    resp = client.put('car/carUpdate/5234',json =car_4)
    # print(resp.json)
    assert resp.json['code'], 400
    assert resp.json['message'], 'bad json'


def test_get_car():

    resp = client.get('car/car/982')
    print(resp.json)
    assert resp.json['id'] is not None
    assert resp.json['reservation_price'] is not None
    assert resp.json['seat_count'] is not None


def test_bad_get_car():

    resp = client.get('car/car/100')
    assert resp.json['code'], 400
    assert resp.json['message'], 'invalid id'

def test_delete_car():

    resp = client.delete('car/car/9823')
    # print(resp.json)
    assert resp.json['carId'] is not None



schema = ReservationCreation()
reservation_2={
"user_id":7022,
"car_id":982,
"amount_of_hours":78,
"reservation_date":"2011-10-05T17:37:46.800Z",
"reservation_end":"2013-11-05T7:37:46.800Z"
}

reservation_3={
"user_ide":0,
"car_id":0,
"amount_of_hours":0,
"reservation_date":"2011-10-05T17:37:46.800Z",
"reservation_end":"2013-11-05T7:37:46.800Z"
}

def test_add_reservation():

    # session.delete(session.query(Reservation).filter_by(car_id=reservation_2["car_id"]).first())
    resp = client.post('/reservation/reservation', json = reservation_2)
    # print(resp.json)
    assert resp.json['reservationId'] is not None

def test_bad_add_reservation():

    resp = client.post('/reservation/reservation', json = reservation_3)
    # print(resp.json)
    assert resp.json['code'], 400
    assert resp.json['message'], 'invalid id'

def test_get_reservation():

    resp = client.get('/reservation/reservation/630')
    # print(resp.json)
    # assert resp.json['code'], 400
    # assert resp.json['message'], 'invalid id'
    assert resp.json["user_id"] is not None
    assert resp.json["car_id"] is not None
    assert resp.json["amount_of_hours"] is not None
    assert resp.json["reservation_date"] is not None
    assert resp.json["reservation_end"] is not None


def test_bad_get_reservation():

    resp = client.get('/reservation/reservation/100')
    # print(resp.json)
    assert resp.json['code'], 400
    assert resp.json['message'], 'There is no such id in database'

def test_bad_delete_reservation():

    resp = client.delete('/reservation/reservation/100')
    print(resp.json)
    assert resp.json['reservationId'] is not None
