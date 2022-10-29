from datetime import datetime

from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class User(Base):
  __tablename__ = 'user'

  id = Column(Integer, primary_key=True, autoincrement="auto")
  username = Column(String(45), unique=True, nullable=False)
  password = Column(String(45), nullable=False)
  firstName = Column(String(45), nullable=False)
  lastName = Column(String(45), nullable=False)
  email = Column(String(45), nullable=False, unique=True)

class Car(Base):
  __tablename__ = 'car'
  id = Column(Integer, primary_key=True, autoincrement="auto")
  seat_count = Column(Integer, nullable=False)
  reservation_price = Column(Float, nullable=False)

class Reservation(Base):
  __tablename__ = 'reservation'

  id = Column(Integer, primary_key=True, autoincrement="auto")
  user_id = Column(Integer, ForeignKey(User.id))
  car_id = Column(Integer, ForeignKey(Car.id))
  amount_of_hours = Column(Integer, nullable=False)
  reservation_date = Column(DateTime, nullable=False)
  reservation_end = Column(DateTime, nullable=False)

  reservation1 = relationship(User, backref='reservation', lazy="joined", foreign_keys=[user_id])
  reservation2 = relationship(Car, backref='reservation', lazy="joined", foreign_keys=[car_id])


# Base.metadata.create_all(engine)