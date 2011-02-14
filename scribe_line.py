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

[USAGE] tail -f /var/log/any.log | scribe_line.py CATEGORY_NAME HOSTNAME PORT [HOSTNAME2 PORT2 [...]]'''

import sys
import os
import time
import fcntl
# import functools
import signal
import random

import re
import warnings

random.seed()

sys.path = [os.path.dirname(__file__)] + sys.path

DEFAULT_RETRY_LOG_WATCH = 0.5
DEFAULT_RETRY_CONNECT = 3
DEFAULT_SIZE_LOGS_BUFFERED = 100

# DEFAULT_RECONNECT_SECONDS = 1800 # 30min.
DEFAULT_RECONNECT_SECONDS = 10 # now testing....


from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport.TTransport import TTransportException

# disable buffering and re-open in NONBLOCK MODE
sys.stdin.close()
stdin_obj = os.fdopen(0, 'r', 0)
fcntl.fcntl(stdin_obj, fcntl.F_SETFL, os.O_NONBLOCK)


if len(sys.argv) < 4:
    sys.exit("Invalid arguments.\n" + __doc__)

category = sys.argv[1]
connect_to_list = []
for i in range(2, len(sys.argv), 2):
    connect_to_list.append([sys.argv[i], sys.argv[i+1]])


class ReloadSignalException(Exception):
    pass

def signal_handler(signum, frame):
    raise ReloadSignalException, "received signal %d. re-connect to server..."
    
signal.signal(signal.SIGHUP, signal_handler)


def with_exception_trap(func):
    # @functools.wraps
    def wrapping_try_except(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except TTransportException, ttex:
            if ttex.type == TTransportException.UNKNOWN:
                pass
            elif ttex.type == TTransportException.NOT_OPEN:
                pass
            elif ttex.type == TTransportException.ALREADY_OPEN:
                pass
            elif ttex.type == TTransportException.TIMED_OUT:
                pass
            elif ttex.type == TTransportException.END_OF_FILE:
                pass
            else:
                raise ttex
            return None
    return wrapping_try_except


@with_exception_trap
def transport_open(host, port):
    sock = TSocket.TSocket(host=host, port=int(port))
    transport = TTransport.TFramedTransport(sock)
    protocol = TBinaryProtocol.TBinaryProtocol(trans=transport, strictRead=False, strictWrite=False)
    client = scribe.Client(iprot=protocol, oprot=protocol)
    transport.open()
    return (client, transport)


buffered_log_lines = []

@with_exception_trap
def mainloop(host_port_pair_list):
    transport = None
    client = None
    amp = 0
    for host, port in host_port_pair_list:
        result = transport_open(host, port)
        if result:
            client, transport = result
            break
        amp = amp + 1
    if not client:
        return

    reconnect_time = time.time() + DEFAULT_RECONNECT_SECONDS + (amp * random.randint(-5,5))
    try:
        try:
            while True:
                global buffered_log_lines
                testing_format = re.compile("\d\d:\d\d:\d\d 1111111111")

                if time.time() > reconnect_time:
                    buffered_log_lines.append("reconnected!!!\n")
                    break

                if len(buffered_log_lines) < 1:
                    try:
                        while len(buffered_log_lines) < DEFAULT_SIZE_LOGS_BUFFERED:
                            line = stdin_obj.readline()
                            if not testing_format.match(line):
                                warnings.warn("NOT complete line: " + line)
                            buffered_log_lines.append()
                    except IOError:
                        if len(buffered_log_lines) == 0 or (len(buffered_log_lines) == 1 and buffered_log_lines[0] == ''):
                            buffered_log_lines = []
                            time.sleep(DEFAULT_RETRY_LOG_WATCH)
                            continue
                log_entries = [scribe.LogEntry(category=category, message=line) for line in buffered_log_lines]

                while True:
                    result = client.Log(messages=log_entries)
                    if result == scribe.ResultCode.OK:
                        buffered_log_lines = []
                        break
                    elif result == scribe.ResultCode.TRY_LATER:
                        time.sleep(DEFAULT_RETRY_CONNECT)
                    else:
                        raise TTransportException, TTransportException.UNKNOWN, "Unknown result code: %d." % result
        except ReloadSignalException:
            pass # ignore
    finally:
        transport.close()

while True:
    mainloop(connect_to_list)
    time.sleep(DEFAULT_RETRY_CONNECT)
