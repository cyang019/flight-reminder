import os
from scanner.airlines import search_korean_air_date_range
from flights_db import create_db

FRIDAYS = [
  '2020-07-17', '2020-07-24', '2020-07-31',
  '2020-08-07', '2020-08-14', '2020-08-21', '2020-08-28',
  '2020-09-04', '2020-09-11', '2020-09-18', '2020-09-25',
  '2020-10-02', '2020-10-09', '2020-10-16', '2020-10-23', '2020-10-30',
  '2020-11-06', '2020-11-13', '2020-11-20'
]
# FRIDAYS = [
#   '2020-10-23', '2020-10-30'
# ]

DBNAME = 'flights'


def scan():
  dates = FRIDAYS
  params = {
    'orig': 'Seoul/Incheon(ICN)',
    'dest': 'Shenyang(SHE)',
    'dates': dates,
    'db_name': DBNAME
  }
  while True:
    search_korean_air_date_range(**params)
  

def main():
  try:
    create_db(DBNAME)
  except Exception as e:
    print(e)
  scan()
  


if __name__ == '__main__':
  main()
