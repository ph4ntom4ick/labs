from flask import Flask
# from models import *
from manager import DBManager
import datetime


from api.user import app as usrbl
from api.car import app as carbl
from api.reservation import app as rsvbl


app= Flask(__name__)

app.register_blueprint(usrbl,url_prefix= "/user")
app.register_blueprint(carbl,url_prefix= "/car")
app.register_blueprint(rsvbl,url_prefix= "/reservation")





























# from models import *
# from manager import DBManager
# import datetime

# if __name__ == '__main__':
#     #creation of db session
#     db = DBManager()
#     session = db.session()

#     user1 = User(id=1, username='sadfgf',password="kurwa", firstName="shozapizdec", lastName="hzvash", email="shozapizdec@gmail")

#     # user2 = UserSchema(iduser=2, username='nast', name="Anastasia", surname="Mor", email="exam1@gmail",
#     #             password="password1", phone="765854", drive_license="A")


#     car1 = Car(id=1, seat_count=4,  reservation_price=123)
#     # car2 = Car(idcar=2, mark="BMW", category="crossover", price=7685, transmission="Automat", status='Unavailable')
#     # car3 = Car(idcar=3, mark="Volkswagen", category="crossover", price=3498, transmission="Automat", status='Available')

#     # orders1 = OrderSchema(idorders=1, renttime=datetime.datetime(2022, 5, 2, 11, 7, 10), renttime_start=datetime.datetime(2022, 5, 2, 15, 25, 3),
#     #                 renttime_end=datetime.datetime(2022, 5, 2, 13, 12, 12), id_iduser=1, id_idcar=1)

#     # orders2 = OrderSchema(idorders=2, renttime=datetime.datetime(2022, 6, 12, 9, 7, 10), renttime_start=datetime.datetime(2022, 6, 13, 9, 25, 3),
#     #                 renttime_end=datetime.datetime(2022, 6, 15, 13, 12, 12), id_iduser=2, id_idcar=3)
#     #
#     # orders3 = Orders(idorders=3, renttime=datetime.datetime(2022, 5, 12, 9, 7, 10), renttime_start=datetime.datetime(2022, 6, 13, 9, 25, 3),
#     #                 renttime_end=datetime.datetime(2022, 6, 15, 13, 12, 12), id_iduser=1, id_idcar=3)


#     session.add(user1)
#     session.commit()
#     # session.add(user2)
#     # session.commit()
#     session.add(car1)
#     session.commit()
#     # session.add(car2)
#     # session.commit()
#     # session.add(car3)
#     # session.commit()
#     # session.add(orders1)
#     # session.commit()
#     # session.add(orders2)
#     # session.commit()
#     # session.add(orders3)
#     #
#     # session.commit()
#     session.close()