import sys, os
sys.path.append(os.path.join('..', '..', 'Waldo'))

from lib import Waldo
from emitted import Pong
import time

def pong_connected(endpoint):
    print '\nPong endpoint is connected!\n'

Waldo.tcp_accept(
    Pong, 'localhost',6767, connected_callback=pong_connected)

time.sleep(5)
