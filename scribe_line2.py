#!/usr/bin/env python
# -*- coding: utf-8 -*-

##  Copyright (c) 2010 tagomrois (TAGOMORI Satoshi) at livedoor.jp
##
##  Licensed under the Apache License, Version 2.0 (the "License");
##  you may not use this file except in compliance with the License.
##  You may obtain a copy of the License at
##
##      http://www.apache.org/licenses/LICENSE-2.0
##
##  Unless required by applicable law or agreed to in writing, software
##  distributed under the License is distributed on an "AS IS" BASIS,
##  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
##  See the License for the specific language governing permissions and
##  limitations under the License.

'''scribe_line.py: log transfer script with scribe

[USAGE] tail -f /var/log/any.log | scribe_line.py HOSTNAME PORT CATEGORY_NAME
            -x: discard logs from buffer when connection to scribe server lost'''

import sys, os, time
sys.path = [os.path.dirname(__file__)] + sys.path

DEFAULT_RETRY_WAIT = 3

from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport.TTransport import TTransportException

if len(sys.argv) != 4:
    sys.exit("Invalid arguments.\n" + __doc__)

host = sys.argv[-3]
port = sys.argv[-2]
category = sys.argv[-1]

inbuffer_logs = []

while True:
    lines = sys.stdin.readlines(500)

    try:
        sock = TSocket.TSocket(host=host, port=int(port))
        transport = TTransport.TFramedTransport(sock)
        protocol = TBinaryProtocol.TBinaryProtocol(trans=transport, strictRead=False, strictWrite=False)
        client = scribe.Client(iprot=protocol, oprot=protocol)
        transport.open()
        log_entry = scribe.LogEntry(category=category, message=line)
        while True:
            result = client.Log(messages=lines)
            if result == scribe.ResultCode.OK:
                break
            elif result == scribe.ResultCode.TRY_LATER:
                time.sleep(DEFAULT_RETRY_WAIT)
            else:
                inbuffer_logs.insert(0, line)
                raise TTransportException, TTransportException.UNKNOWN, "Unknown result code: %d." % result
        transport.close()
    except TTransportException, ttex:
        if ttex.type == TTransportException.UNKNOWN:
            print "transferring, UNKNOWN error... retry after sleep"
            time.sleep(DEFAULT_RETRY_WAIT)
        elif ttex.type == TTransportException.NOT_OPEN:
            print "transferring, NOT_OPEN error... retry after sleep"
            time.sleep(DEFAULT_RETRY_WAIT)
        elif ttex.type == TTransportException.ALREADY_OPEN:
            print "transferring, ALREADY_OPEN error... retry after sleep"
            time.sleep(DEFAULT_RETRY_WAIT)
        elif ttex.type == TTransportException.TIMED_OUT:
            print "transferring, TIMED_OUT error... retry after sleep"
            time.sleep(DEFAULT_RETRY_WAIT)
        elif ttex.type == TTransportException.END_OF_FILE:
            print "transferring, EOF error... retry after sleep"
            time.sleep(DEFAULT_RETRY_WAIT)
        else:
            raise
    if len(''.join(lines)) < 500 or sys.stdin.closed:
        break
