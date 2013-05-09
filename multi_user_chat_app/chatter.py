import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from lib import Waldo
from emitted import ChatterA, ChatterB
import time, Queue

# Global Variables
HOSTNAME = '127.0.0.1'
AWS_IP = '54.235.158.36'
PORT = 6767
SLEEP_TIME = .2
NUM_CONNECTIONS = 2
quit = False
messages = Queue.Queue()
connections = list()

# Function Definitions
def display_msg(endpoint, msg): 
  ''' 
  Displays a message received by an endpoint on the screen.
  '''
  global quit
  print ('RECEIVED: ' + msg)
  if (msg == 'quit'):
    quit = True

def queue_msg(endpoint, msg):
  '''
  Adds message received to a global queue of messages.
  '''
  global messages
  messages.put((endpoint, msg))

def run_chatter_a():
  '''
  Runs an accepting single chatter.
  '''
  global quit
  Waldo.tcp_accept(ChatterA, HOSTNAME, PORT, display_msg,
      connected_callback=listen_for_user_input)
  while True:
    if quit:
      break
    time.sleep(SLEEP_TIME)

def run_chatter_b():
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
  print "Type 'quit' to exit." 
  while True:
    msg_to_send = str(raw_input())
    endpoint_obj.send_msg_to_other_side(msg_to_send)
    if msg_to_send == "quit":
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
  print HOSTNAME, PORT
  if (sys.argv[1] == 'a'):
    run_chatter_a()
  elif sys.argv[1] == 'chat':
    run_chatter_b()
  elif sys.argv[1] == 'server':
    run_server()
