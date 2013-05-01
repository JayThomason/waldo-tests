import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from lib import Waldo
from emitted import ChatterA, ChatterB
import time
HOSTNAME = '127.0.0.1'
PORT = 6922
SLEEP_TIME = .1

def display_msg(endpoint, msg): 
  # note: a more sophisticated app might write to a gui instead.
  print ('MSG: ' + msg)

def run_chatter_a():
  # runs in accept mode
  chatter_a = Waldo.tcp_accept(ChatterA, HOSTNAME, PORT, display_msg)
  listen_for_other_side(chatter_a)

def run_chatter_b():
  chatter_b = Waldo.tcp_connect(ChatterB, HOSTNAME, PORT, display_msg)
  listen_for_user_input(chatter_b)

def listen_for_other_side(endpoint_obj):
  '''
  Continuously poll to see if there's a message from other side to display.
  '''
  while True:
    time.sleep(SLEEP_TIME)
    msg = endpoint_obj.service_signal()
    if msg is not None:
      display_msg(endpoint_obj, msg)
    elif msg == 'quit':
      break

    

def listen_for_user_input(endpoint_obj):
  print "Type 'quit' to exit." 
  while True:
    msg_to_send = str(raw_input('message: '))
    endpoint_obj.send_msg_to_other_side(msg_to_send)
    if msg_to_send == "quit":
      break

if __name__ == '__main__':
  '''
  Passing in argument 'a' starts ChatterA listening.

  Executing another process passing in 'b' starts ChatterB taking input 
  from user.
  '''
  if (sys.argv[1] == 'a'):
    run_chatter_a()
  else:
    run_chatter_b()
