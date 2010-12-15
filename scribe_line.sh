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

$SCRIBE_LINE_CMD=`dirname $0`/scribe_line.py
$SCRIBE_SERVER="10.0.195.90" # scribe-test.admin 
$SCRIBE_PORT=1464            # 1463 ?
$DEFAULT_CATEGORY="unknown"

$logs_dir=$1
$basename=$2
$category=$3
if [ x"$category" = "x" ]; then
    $category=$DEFAULT_CATEGORY
fi

function filename_follow_recent {
    log_directory=$1
    base_filename=$2
    find $log_directory -name $base_filename'*' -type f | xargs ls -t | head -1
}

tail -c +0 -F `filename_follow_recent $logs_dir $basename` | $SCRIBE_LINE_CMD $SCRIBE_SERVER $SCRIBE_PORT $category
