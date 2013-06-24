import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from waldo.lib import Waldo
from emitted import EndpointA, EndpointB
import time, subprocess
HOSTNAME = '0.0.0.0'
WAIT_TIME = 10
PORT = 6767

def retrieve_list(endpoint_obj):
  '''Returns the output of the users unix command as a string.'''
  return subprocess.check_output(['users'])

def cb(endpoint_obj):
  print 'Connected.'

def tell():
  '''Accepts incoming requests for retrieve list.'''
  Waldo.tcp_accept(EndpointB, HOSTNAME, PORT, retrieve_list, 
      connected_callback=cb)
  time.sleep(WAIT_TIME)

def ask():
  '''
  Asks the listening endpoint for a list of its users, parses it,
  and prints a unique list of users logged on at the other 
  endpoint. 
  '''
  sender = Waldo.tcp_connect(EndpointA, HOSTNAME, PORT)
  print 'Users on', HOSTNAME
  users = sender.ask_for_list()
  user_list = users.strip('\n').split(' ')
  user_list = list(set(user_list))
  for user in user_list:
    print '\t', user


if __name__ == '__main__':
  '''
  Passing in argument 'tell' starts the listening side.
  Passing in argument 'ask' starts the asking side.
  '''
  if len(sys.argv) <= 1 or len(sys.argv) > 3:
    print 'Correct usage: python who.py [ask|tell hostname]'
  if len(sys.argv) == 3:
    HOSTNAME = sys.argv[2]
  if sys.argv[1] == 'ask':
    ask()
  elif sys.argv[1] == 'tell':
    tell()
