#!/usr/bin/env python
# -*- coding:utf-8 -*-

import sys
import os
sys.path = [os.path.dirname(__file__) + '/..'] + sys.path

from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from scribe import scribe

if len(sys.argv) == 2:
  category = sys.argv[1]
  host = '127.0.0.1'
  port = 1463
elif len(sys.argv) == 4 and sys.argv[1] == '-h':
  category = sys.argv[3]
  host_port = sys.argv[2].split(':')
  host = host_port[0]
  if len(host_port) > 1:
    port = int(host_port[1])
  else:
    port = 1463
else:
  sys.exit('usage (message is stdin): scribe_cat [-h host[:port]] category')

logentries = []
while True:
    line = sys.stdin.readline()
    if line == '':
        break
    if not line.endswith('\n'):
        line += '\n'
    logentries.append(scribe.LogEntry(category=category, message=line))

socket = TSocket.TSocket(host=host, port=port)
transport = TTransport.TFramedTransport(socket)
protocol = TBinaryProtocol.TBinaryProtocol(trans=transport, strictRead=False, strictWrite=False)
client = scribe.Client(iprot=protocol, oprot=protocol)

transport.open()
result = client.Log(messages=logentries)
transport.close()

if result == scribe.ResultCode.OK:
  sys.exit()
elif result == scribe.ResultCode.TRY_LATER:
  print >> sys.stderr, "TRY_LATER"
  sys.exit(84)  # 'T'
else:
  sys.exit("Unknown error code.")
