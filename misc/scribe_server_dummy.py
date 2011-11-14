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

if len(sys.argv) == 2:
  port = int(sys.argv[1])
else:
  sys.exit('usage (message is stdin): scribe_client_dummy.py port')

class ScribeDummyHandler:
    def __init__(self):
        self.counter = 0

    def Log(self, messages):
        msgs = {}
        for m in messages:
            if m.category not in msgs:
                msgs[m.category] = 0
            msgs[m.category] += 1
        for k in msgs.keys():
            print k + ':' + str(msgs[k])
        return ttypes.ResultCode.OK

handler = ScribeDummyHandler()
processor = scribe.Processor(handler)
transport = TSocket.TServerSocket(port)
tfactory = TTransport.TFramedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory(strictRead=False, strictWrite=False) # non-strict read/write for scribe

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print 'Starting scribed dummy server...'
server.serve()
print 'done.'
