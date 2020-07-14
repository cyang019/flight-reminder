from flights_db import select_july_aug_sep, select_july_aug_sep_test
from email_sender import create_n_send_message


TABLENAME = 'flights'
RECEIVERS = ['yangcnju@gmail.com', '247594213@qq.com']

def flight_tuple_to_str(flight_tuple):
  date_flight = flight_tuple[0]
  price = flight_tuple[1]
  orig, dest = flight_tuple[5], flight_tuple[6]
  found_time = flight_tuple[9]
  msg = f'{orig} - {dest} {date_flight} {price} [found on {found_time}]'
  return msg

def construct_message(flights):
  print(flights)
  flights_str = []
  for i, flight in enumerate(flights):
    flight_str = flight_tuple_to_str(flight)
    line = f'[{i}] {flight_str}'
    flights_str.append(line)
  body = '\n'.join(flights_str)
  message = f'flights:\n{body}'
  return message

def alert_on_valuable_flight():
  result = select_july_aug_sep(TABLENAME)
  if len(result) > 0:
    message = construct_message(result)
    receivers = RECEIVERS[:]
    title = 'flight found'
    sender = 'chen.yang.bytes@gmail.com'
    for receiver in receivers:
      create_n_send_message(sender, receiver, title, message)
      print(f'email sent to {receiver}')

def alert_on_valuable_flight_test():
  result = select_july_aug_sep_test(TABLENAME)
  if len(result) > 0:
    message = construct_message(result)
    receivers = ['yangcnju@gmail.com']
    title = 'flight found'
    sender = 'chen.yang.bytes@gmail.com'
    for receiver in receivers:
      create_n_send_message(sender, receiver, title, message)
