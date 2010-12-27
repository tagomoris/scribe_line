#!/bin/bash
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

SCRIBE_LINE_CMD=$(dirname $0)"/scribe_line.py"
MD5SUM="/usr/bin/md5sum"
if [ ! -x $MD5SUM ]; then
    MD5SUM="/sbin/md5"
fi

DEFAULT_CATEGORY="unknown"

PRIMARY_SERVER="10.0.195.90"
PRIMARY_PORT="1463"

SECONDARY_SERVER="10.0.195.90"
SECONDARY_PORT="1464"

logs_dir=$1
if [ ! -e $logs_dir ]; then
    exit 1;
fi
basename=$2
if [ x"$basename" = "x" ]; then
    exit 1;
fi

category=$3
if [ x"$category" = "x" ]; then
    category=$DEFAULT_CATEGORY
fi

target_checksum=`echo -n "$logs_dir/$basename" | $MD5SUM`
tail_file_path=`find $logs_dir -name $basename'*' -type f | xargs ls -t | head -1`

tail -F $tail_file_path | $SCRIBE_LINE_CMD $category $PRIMARY_SERVER $PRIMARY_PORT $SECONDARY_SERVER $SECONDARY_PORT $target_checksum
exit $?
