import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from lib import Waldo
from emitted import ChatterA, ChatterB
import time, Queue

# Global Variables
HOSTNAME = '127.0.0.1'
# AWS_IP = '54.235.158.36'
PORT = 6767
SLEEP_TIME = .2
ANON = 'anon'
quit = False
messages = Queue.Queue()
connections = list()

# Function Definitions
def display_msg(endpoint, msg): 
  ''' 
  Displays a message received by an endpoint on the screen.
  '''
  global quit
  print (msg)
  if (msg == 'quit'):
    quit = True

def queue_msg(endpoint, msg):
  '''
  Adds message received to a global queue of messages.
  '''
  global messages
  messages.put((endpoint, msg))

def run_chatter_client():
  ''' 
  Runs a connecting single chatter. Connects to the chat server.
  '''
  chatter_b = Waldo.tcp_connect(ChatterB, HOSTNAME, PORT, display_msg)
  listen_for_user_input(chatter_b)

def run_server():
  '''
  Runs the multi-connection chat server.
  '''
  global quit
  Waldo.tcp_accept(ChatterA, HOSTNAME, PORT, queue_msg,
      connected_callback=newConnectionCallback)
  listen_for_messages()

def newConnectionCallback(endpoint_obj):
  '''
  Establishes a new server-side connection.
  '''
  global connections
  print 'Connection established.'
  connections.append(endpoint_obj)

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
    if msg_to_send != "quit":
      msg_to_send = username + ': ' + msg_to_send
      endpoint_obj.send_msg_to_other_side(msg_to_send)
    else:
      endpoint_obj.send_msg_to_other_side(msg_to_send)
      break

def listen_for_messages():
  '''
  Continuously polls the message queue.
  When the queue has messages, they are sent out to endpoint which
  did not send the original message.
  '''
  global messages, connections
  print "New connection."
  while True:
    if not messages.empty():
      msg_pair = messages.get()
      for endpoint_obj in connections:
        if msg_pair[1] == 'quit' and endpoint_obj == msg_pair[0]:
          connections.remove(endpoint_obj)
          print 'Endpoint disconnected: ', endpoint_obj
        if endpoint_obj != msg_pair[0]:
          endpoint_obj.send_msg_to_other_side(msg_pair[1])
      print msg_pair
    else:
      time.sleep(SLEEP_TIME)


# Main
if __name__ == '__main__':
  '''
  Passing in argument 'a' starts ChatterA listening.

  Executing another process passing in 'b' starts ChatterB taking input 
  from user.
  '''
  if (len(sys.argv) == 1):
    print 'Correct usage: python chatter.py [a|b] [aws]'
  elif (len(sys.argv) > 2 and sys.argv[1] == 'b'):
    PORT = int(sys.argv[2])
  if sys.argv[1] == 'client':
    print HOSTNAME, PORT
    run_chatter_client()
  elif sys.argv[1] == 'server':
    run_server()
