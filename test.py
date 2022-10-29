from models import User, Reservation, Car
from datetime import datetime, timedelta
import mysql.connector

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

lab6ap = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="lviv16"
)

engine = create_engine('mysql://root:lviv16@127.0.0.1:3306/shos_yak_car_reservation', pool_pre_ping=True)
SessionFactory = sessionmaker(bind=engine)
Session = scoped_session(SessionFactory)

session = Session()

user = User(id = 1, username = 'testlogin', password = 'testpass', 
    firstName = 'fname', lastName = 'lname', email = 'test@email.com')
car = Car(id = 1,  seat_count = 20, reservation_price = 200.0)
reservation = Reservation(id = 1, user_id = 1, car_id = 1, 
    amount_of_hours = 3, reservation_date = datetime(2022, 10, 22), reservation_end = datetime(2022, 10, 22)+timedelta(hours = 3))

session.add(user)
session.add(car)
session.add(reservation)
session.commit()
session.close()