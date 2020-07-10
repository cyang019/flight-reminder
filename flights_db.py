from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, DateTime, MetaData, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.sql import select
from datetime import datetime

Base = declarative_base()
dbname = 'flights'
engine = create_engine(f'sqlite:///{dbname}.sqlite3')
Base.metadata.bind = engine
Session = scoped_session(sessionmaker(bind=engine))


class Flight(Base):
  __tablename__ = 'flights'
  # id = Column(Integer, primary_key=True)
  date_flight = Column(String(100), primary_key=True)     # 2020-08-20:UA857
  flight_fare = Column(String(100))
  flight_class = Column(String(50))
  flight_stop = Column(String(50))
  flight_duration = Column(String(50))
  flight_from = Column(String(200))
  flight_to = Column(String(200))
  flight_from_time = Column(String(100))
  flight_to_time = Column(String(100))
  timestamp = Column(DateTime)

def create_db(dbname):
  # engine = create_engine(f'sqlite:///{dbname}.sqlite3')
  Base.metadata.create_all(engine)

def insert_to_db(dbname, date, flight_number, flight_fare,
                 flight_class='', flight_stop='',
                 flight_duration='', flight_from='',
                 flight_to='', flight_from_time='', flight_to_time='',
                 timestamp=None):
  engine = create_engine(f'sqlite:///{dbname}.sqlite3')
  # Base.metadata.bind = engine
  # DBSession = sessionmaker(bind=engine)
  session = Session()
  key = f'{date}:{flight_number}'
  if timestamp is None:
    timestamp = datetime.now()
  new_flight = Flight(date_flight=key, flight_fare=flight_fare,
    flight_class=flight_class, flight_stop=flight_stop, flight_duration=flight_duration,
    flight_from=flight_from, flight_to=flight_to,
    flight_from_time=flight_from_time, flight_to_time=flight_to_time,
    timestamp=timestamp)
  session.merge(new_flight)
  session.commit()
  session.flush()
  session.close()

def select_all(dbname):
  # engine = create_engine(f'sqlite:///{dbname}.sqlite3')
  # Session = sessionmaker(bind=engine)
  with engine.connect() as con:
    result_proxy = con.execute(f'SELECT * FROM {dbname}')
    result = [row for row in result_proxy]
  return result




