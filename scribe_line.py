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

[USAGE] tail -f /var/log/any.log | scribe_line.py [-r READBUF_SIZE] CATEGORY_NAME HOSTNAME PORT [HOSTNAME2 PORT2 [...]]'''

import sys
import os
import time
import errno
import socket
import fcntl
# import functools
import signal
import random

random.seed()

sys.path = [os.path.dirname(__file__)] + sys.path

DEFAULT_READ_BUFFER_SIZE = 20480

DEFAULT_RETRY_LOG_WATCH = 0.1
DEFAULT_RETRY_CONNECT = 3
DEFAULT_SIZE_LOGS_BUFFERED = 100

DEFAULT_RECONNECT_SECONDS = 1800 # 30min.

from scribe import scribe
from thrift.transport import TTransport, TSocket
from thrift.protocol import TBinaryProtocol
from thrift.transport.TTransport import TTransportException

## OPTIONS
READ_BUFFER_SIZE = DEFAULT_READ_BUFFER_SIZE
if sys.argv[1] == '-r':
    READ_BUFFER_SIZE = int(sys.argv[2])
    del sys.argv[1:3]

if len(sys.argv) < 4:
    sys.exit("Invalid arguments.\n" + __doc__)

category = sys.argv[1]
connect_to_list = []
for i in range(2, len(sys.argv), 2):
    connect_to_list.append([sys.argv[i], sys.argv[i+1]])

# disable buffering and re-open in NONBLOCK MODE
sys.stdin.close()
stdin_obj = os.fdopen(0, 'r', 0)
fcntl.fcntl(stdin_obj, fcntl.F_SETFL, os.O_NONBLOCK)

class BrokenPipeException(Exception):
    pass

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
        except socket.error, e:
            if e[0] == errno.EPIPE:
                pass
            elif e[0] == errno.ECONNRESET:
                pass
            else:
                raise e
            return None
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


continuous_line = None
buffered_log_lines = []

def drain():
    global continuous_line
    global buffered_log_lines
    global stdin_obj
    line = None
    while len(buffered_log_lines) < DEFAULT_SIZE_LOGS_BUFFERED:
        line = stdin_obj.read(READ_BUFFER_SIZE)
        if len(line) < 1: # maybe eof, means broken input pipe (tail process died)
            try:
                stdin_obj.close()
                print "reopening stdin ..."
                stdin_obj = os.fdopen(0, 'r', 0)
                fcntl.fcntl(stdin_obj, fcntl.F_SETFL, os.O_NONBLOCK)
            except OSError:
                raise BrokenPipeException, 'broken input pipe, maybe tail process died'
            continue
        while True:
            newline_pos = line.find("\n")
            if newline_pos < 0:
                break
            pos = newline_pos + 1
            if continuous_line:
                buffered_log_lines.append(continuous_line + line[0:pos])
                continuous_line = None
            else:
                buffered_log_lines.append(line[0:pos])
            line = line[pos:]
        if len(line) > 0:
            continuous_line = line
        line = None

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

    global continuous_line
    global buffered_log_lines
    reconnect_time = time.time() + DEFAULT_RECONNECT_SECONDS + (amp * random.randint(-5,5))
    try:
        try:
            while True:
                if time.time() > reconnect_time:
                    break

                if len(buffered_log_lines) < 1:
                    try:
                        drain()
                    except IOError:
                        if len(buffered_log_lines) == 0:
                            time.sleep(DEFAULT_RETRY_LOG_WATCH)
                            continue

                if len(buffered_log_lines) < 1:
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

print "scribe_line.py exiting... why?"
