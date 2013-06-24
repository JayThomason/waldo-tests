import sys, os
sys.path.append(os.path.join('..', '..', 'Waldo'))

from waldo.lib import Waldo
from emitted import Ping
import time

ping = Waldo.tcp_connect(Ping, 'localhost', 6767)

print ('\nThis is result of ping seq: ' + str(ping.ping_seq(0)))
