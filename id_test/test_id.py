import sys, os
sys.path.append(os.path.join('..','..','Waldo'))

from waldo.lib import Waldo
from emitted import IdTester

HOSTNAME = '0.0.0.0'
PORT = 6767

if __name__ == '__main__':
  Waldo.tcp_accept(IdTester, HOSTNAME, PORT)
  id_tester = Waldo.tcp_connect(IdTester, HOSTNAME, PORT)
  print "id : ", id_tester.get_id()
