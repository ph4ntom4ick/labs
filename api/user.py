from flask import Blueprint, Flask, request, Response, make_response

from werkzeug.security import check_password_hash, generate_password_hash

from labs.manager import *
from labs.models import User, Car
from labs.schemas.user import UserCreation
import random

from flask import jsonify, abort
from marshmallow import ValidationError
import sqlalchemy.exc as sql_exception
from flask_jwt_extended import JWTManager


from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import current_user
# from flask_jwt_extended import user_identity_loader
# from flask_jwt_extended import user_lookup_loader
API_KEY = 'MY_API_KEY'


app = Blueprint('Saturn', __name__)
# app = Flask(__name__)



jwt = None


session = DBManager().session()

# @jwt.user_identity_loader
# def user_identity_lookup(user):
#     return user.id

# @jwt.user_lookup_loader
# def user_lookup_callback(_jwt_header, jwt_data):
#     identity = jwt_data["sub"]
#     return session.query(User).filter_by(id=identity).one_or_none()

@app.route('/user', methods=['POST'])
def user()->Response:

    request_json = request.get_json()
    try:
        new_user = UserCreation().load(request_json)
        password_hash = generate_password_hash(new_user.get('password'))
        user_record = User(
            id=random.randint(1, 10000),
            username=new_user.get('username'),
            password=password_hash,
            firstName=new_user.get('firstName'),
            lastName=new_user.get('lastName'),
            email=new_user.get('email')
        )
        session.add(user_record)
        session.commit()
    except (ValidationError, sql_exception.IntegrityError) as e:
        response = {
            "code": 400,
            "message": f"Server crashed with the following error: {str(e)}"
        }
        return make_response(response, 400)
    respose = make_response({"userId": user_record.id}, 200)
    return respose


@app.route('/user/login', methods=['GET'])
def login_user():

    username = request.args.get("username")
    password = request.args.get("password")
    # print(username,password)

    user: User = session.query(User).filter_by(username = username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token)
    else:
        response = {
            "code": 401,
            "message": "Wrong credentials"
        }
        return make_response(response, 400)


@app.route('/user/logout', methods=['GET'])
def logout_user():
    response = {
        "code": 200,
        "message": "Logged out user"
    }
    return make_response(response, 200)



@app.route("/user/<user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id) -> Response:
    
    if current_user==user_id:
        return jsonify(message= "acces forbidden "),403
    user_record: User = session.query(User).filter(user_id == User.id).first()

    if not user_record:
        response = {
            "code": 400,
            "message": "There is no such id in database"
        }
        return make_response(response, 400)

    respose = make_response(user_record.as_dict(), 200)
    return respose



# @app.route("/user/<user_id>", methods=["PUT"])
# @jwt_required()
# def update_user(user_id) -> Response:

#     if current_user==user_id:
#         return jsonify(message= "acces forbidden "),403
#     request_json = request.get_json()
#     user_record = session.query(User).filter(user_id == User.id).first()
#     if not user_record:
#         response = {
#             "code": 400,
#             "message": "There is no such user"
#         }
#         return make_response(response, 400)

#     try:
#         # validate request input
#         user = UserCreation().load(request_json)
#         password_hash = generate_password_hash(user.get('password'))
#         user_record={
#             "name": user.get('firstName'),
#             "surname": user.get('lastName'),
#             "password": password_hash,
#         }
#         # create database record
#         session.query(User).filter(user_id == User.id).update(user_record)
#         session.commit()

#     except (ValidationError, sql_exception.IntegrityError) as e:
#         response = {
#             "code": 400,
#             "message": f"Server crashed with the following error: {str(e)}"
#         }
#         return make_response(response, 400)

#     respose = make_response({"userId": user_id}, 200)
#     return respose

# @app.route("/user/<user_id>", methods=["DELETE"])
# @jwt_required()
# def delete_user(user_id) -> Response:

#     if current_user==user_id:
#         return jsonify(message= "acces forbidden "),403
#     api_key_header = request.headers.get('api_key')
#     if False:
#         response = {
#             "code": 400,
#             "message": "Not allowed. Provide a valid api_key header"
#         }
#         return make_response(response, 400)

#     session.query(User).filter(user_id == User.id).delete()
#     session.commit()

#     respose = make_response({"userId": user_id}, 200)
#     return respose




def get_blueprint(current_app):
    jwt = JWTManager(current_app)
    return app

# if __name__ == '__main__':
#     app.run(port=5001)

    
# @app.route("/user", methods=["POST"])
# def add_car() -> Response:
#
#     request_json = request.get_json()
#     try:
#         user = User().load(request_json)
#     except ValidationError as e:
#         response = {
#             "code": 400,
#             "message": f"Server crashed with the following error: {str(e)}"
#         }
#         return make_response(response, 400)
#
#     respose = make_response({"userId": 101}, 200)
#     return respose
#
# @app.route("/user/login", methods=["GET"])
# def log_user_in() -> Response:
#
#     username = request.args.get("username")
#     password = request.args.get("password")
#
#     response = make_response("Logged in", 200)  # Data, Status Code
#     return response
#
# @app.route("/user/logout", methods=["GET"])
# def log_user_out() -> Response:
#
#     response = make_response("Logged out", 200)  # Data, Status Code
#     return response
#
# @app.route("/user/getbookedcar", methods=["GET"])
# def get_booked_cars() -> Response:
#
#     bookings = [Order().load(DEFAULT_ORDER), Order().load(DEFAULT_ORDER)]
#     response = make_response(bookings, 200)  # Data, Status Code
#     return response
#
#
# @app.route("/user/{userId}", methods=["PUT"])
# def update_user() -> Response:
#         userId = request.args.get("userId")
#         response = make_response("Updated", 200)
#         return response
#
# @app.route('/user/{userId}', methods=['DELETE'])
# def delete_user():
#     session.query(User).filter(User.id == id).delete()
#     session.commit()
#     return jsonify({'Message': 'There is no such group now!'})

# if __name__ == '__main__':
#     app.run(port=5001)