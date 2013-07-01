import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from waldo.lib import Waldo
from server.emitted import Server
from client.emitted import Client, ClientHandler
import time

# Global Variables
HOSTNAME = '0.0.0.0'
PORT = 6767
SLEEP_TIME = 2
ANON = 'anon'
server = None

# Function Definitions
def display_msg(endpoint, msg): 
  ''' 
  Displays a message received by an endpoint on the screen.
  '''
  print (msg)

def display_hex_string(endpoint, string):
  '''
  Displays a string as hex character codes separated by colons.
  '''
  print ':'.join(x.encode('hex') for x in string)

def run_chatter_client():
  ''' 
  Runs a connecting single chatter. Connects to the chat server.
  '''
  client = Waldo.tcp_connect(Client, HOSTNAME, PORT, display_msg)
  listen_for_user_input(client)

def run_server():
  '''
  Runs the multi-connection chat server.
  '''
  global server
  # server = Waldo.no_partner_create(Server, display_msg)
  server = Waldo.no_partner_create(Server, display_hex_string)
  print server
  Waldo.tcp_accept(ClientHandler, HOSTNAME, PORT, server, display_msg)
  while True:
    time.sleep(SLEEP_TIME)

def listen_for_user_input(endpoint_obj):
  '''
  Loops continuously listening for user input.
  Returns when the user message is 'quit'.
  '''
  print "Type 'quit' to exit chatroom." 
  username = str(raw_input('Choose a username (blank for anon)'))
  if len(username) == 0:
    username = ANON
  while True:
    msg_to_send = str(raw_input())
    msg_to_send = username + ': ' + msg_to_send
    endpoint_obj.send_msg(msg_to_send)

# Main
if __name__ == '__main__':
  '''
  Passing in 'server' starts the server, passing in 'client' starts up a
  client which connects to the server.

  Optional args include the hostname.
  '''
  if (len(sys.argv) == 1):
    print 'Correct usage: python chatter.py [client|server] [aws]'
  else:
    if (len(sys.argv) > 2 and sys.argv[1] == 'b'):
      HOSTNAME = int(sys.argv[2])
    if sys.argv[1] == 'client':
      run_chatter_client()
    elif sys.argv[1] == 'server':
      run_server()
