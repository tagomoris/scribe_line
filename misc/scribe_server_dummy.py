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

from pprint import pprint

class ScribeDummyHandler:
    def __init__(self):
        self.counter = 0

    def Log(self, messages):
        msgs = len(messages)
        self.counter += msgs
        print 'RECV:' + str(msgs)
        pprint(messages)
        return ttypes.ResultCode.OK

handler = ScribeDummyHandler()
processor = scribe.Processor(handler)
transport = TSocket.TServerSocket(1463)
tfactory = TTransport.TFramedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory(strictRead=False, strictWrite=False) # non-strict read/write for scribe

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print 'Starting scribed dummy server...'
server.serve()
print 'done.'
