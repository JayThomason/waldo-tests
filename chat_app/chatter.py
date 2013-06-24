import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from waldo.lib import Waldo
from emitted import ChatterA, ChatterB
import time
HOSTNAME = '127.0.0.1'
AWS_IP = '54.235.158.36'
PORT = 6767
SLEEP_TIME = .2
quit = False

def display_msg(endpoint, msg): 
  # note: a more sophisticated app might write to a gui instead.
  global quit
  print ('RECEIVED: ' + msg)
  if (msg == 'quit'):
    quit = True

def run_chatter_a():
  # runs in accept mode
  global quit
  Waldo.tcp_accept(ChatterA, HOSTNAME, PORT, display_msg,
      connected_callback=listen_for_user_input)
  while True:
    if quit:
      break
    time.sleep(SLEEP_TIME)

def run_chatter_b():
  chatter_b = Waldo.tcp_connect(ChatterB, HOSTNAME, PORT, display_msg)
  listen_for_user_input(chatter_b)

def listen_for_user_input(endpoint_obj):
  print "Type 'quit' to exit." 
  while True:
    msg_to_send = str(raw_input())
    endpoint_obj.send_msg_to_other_side(msg_to_send)
    if msg_to_send == "quit":
      break

if __name__ == '__main__':
  '''
  Passing in argument 'a' starts ChatterA listening.

  Executing another process passing in 'b' starts ChatterB taking input 
  from user.
  '''
  if (len(sys.argv) == 1):
    print 'Correct usage: python chatter.py [a|b] [aws]'
  elif (len(sys.argv) > 2 and sys.argv[1] == 'b' and sys.argv[2] == 'aws'):
    HOSTNAME = AWS_IP
  if (sys.argv[1] == 'a'):
    run_chatter_a()
  elif sys.argv[1] == 'b':
    run_chatter_b()
