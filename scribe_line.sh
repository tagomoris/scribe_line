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

# USAGE:
# scribe_line.sh [options] category /path/to/logfile primary_server[:port] [secondary_server[:port]]
# OPTIONS:
#    -p pythonpath

PYTHON="/usr/bin/python"

SCRIBE_LINE_CMD=$(dirname $0)"/scribe_line.py"
DEFAULT_PORT=1463

BOOST_MODE=

function usage {
    cat >&2 <<EOF
USAGE:
scribe_line.sh [options] category /path/to/logfile primary_server[:port] [secondary_server[:port]]
OPTIONS:
   -p pythonpath
EOF
}

while getopts "hbp:" flag; do
    case $flag in
        \?) OPT_ERROR=1;;
        h) usage; exit 0;;
        b) BOOST_MODE="-b";;
        p) PYTHON="$OPTARG";;
    esac
done

shift $(( $OPTIND - 1 ))

if [ ! -x "$PYTHON" ]; then
    cat >&2 <<EOF
ERROR: specified python path is not executable: $PYTHON
EOF
    OPT_ERROR=1
fi

category=$1
if [ x"$category" = "x" ]; then
    cat >&2 <<EOF
ERROR: category not specified
EOF
    ARG_ERROR=1
fi

tail_file_path=$2
if [ ! -f "$tail_file_path" ]; then
    cat >&2 <<EOF
ERROR: target log file path not specified or not exists: $tail_file_path
EOF
    ARG_ERROR=1
fi

primary=$3
if [ x"$primary" = "x" ]; then
    cat >&2 <<EOF
ERROR: primary scribed server not specified
EOF
    ARG_ERROR=1
else
    PRIMARY_SERVER=`echo $primary | cut -d : -s -f 1`
    PRIMARY_PORT=`echo $primary | cut -d : -s -f 2`
    if [ x"$PRIMARY_SERVER" = "x" ]; then
        PRIMARY_SERVER=$primary
        PRIMARY_PORT=$DEFAULT_PORT
    fi
fi

secondary=$4
if [ x"$secondary" = "x" ]; then
    SECONDARY_UNSPECIFIED=1
else
    SECONDARY_SERVER=`echo $secondary | cut -d : -s -f 1`
    SECONDARY_PORT=`echo $secondary | cut -d : -s -f 2`
    if [ x"$SECONDARY_SERVER" = "x" ]; then
        SECONDARY_SERVER=$secondary
        SECONDARY_PORT=$DEFAULT_PORT
    fi
fi

if [ x"$OPT_ERROR" != "x" -o x"$ARG_ERROR" != "x" ]; then
    usage
    exit 1
fi

OPT_SLEEP_INTERVAL=
tail -s 1 /dev/null >/dev/null 2>&1
if [ $? eq 0 ]; then
    OPT_SLEEP_INTERVAL="-s 0.1"
fi

if [ $SECONDARY_UNSPECIFIED ]; then
    tail $OPT_SLEEP_INTERVAL -F $tail_file_path | $PYTHON $SCRIBE_LINE_CMD $BOOST_MODE $category $PRIMARY_SERVER $PRIMARY_PORT
else
    tail $OPT_SLEEP_INTERVAL -F $tail_file_path | $PYTHON $SCRIBE_LINE_CMD $BOOST_MODE $category $PRIMARY_SERVER $PRIMARY_PORT $SECONDARY_SERVER $SECONDARY_PORT
fi
exit $?
