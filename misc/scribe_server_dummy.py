#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
sys.path = [os.path.dirname(__file__) + '/..'] + sys.path

from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport.TTransport import TTransportException
from thrift.server import TServer

from scribe import scribe
from scribe import ttypes

verbose = True
port = 1463
if len(sys.argv) == 2:
    port = int(sys.argv[1])
elif len(sys.argv) == 3 and sys.argv[1] == '-q':
    verbose = False
    port = int(sys.argv[2])
else:
    sys.exit('usage (message is stdin): scribe_client_dummy.py [-q] port')

from pprint import pprint

class ScribeDummyHandler:
    def __init__(self):
        self.counter = 0

    def Log(self, messages):
        msgs = {}
        if verbose:
            for m in messages:
                if m.category not in msgs:
                    msgs[m.category] = 0
                msgs[m.category] += 1
            for k in msgs.keys():
                sys.stdout.write(k + ':' + str(msgs[k]) + "\n")
            sys.stdout.flush()
        else:
            self.counter += len(messages)
        return ttypes.ResultCode.OK

handler = ScribeDummyHandler()

processor = scribe.Processor(handler)
transport = TSocket.TServerSocket(port)
tfactory = TTransport.TFramedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory(strictRead=False, strictWrite=False) # non-strict read/write for scribe

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)


import signal

class SIGHUPException(Exception):
    pass

def signal_handler(signum, frame):
    raise SIGHUPException

signal.signal(signal.SIGHUP, signal_handler)

try:
    server.serve()
except:
    pass

sys.stdout.write("\n")
sys.stdout.write("RECV:" + str(handler.counter) + "\n")
sys.stdout.flush()

