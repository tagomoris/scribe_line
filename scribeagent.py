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

'''scribeagent.py: start-stop script for scribe_line.sh.
   find httpd log scripts from config files, and send all of them with scribe_line.sh

[USAGE] scribeagent [start|stop|restart|reload|status]
  reload: send SIGHUP to all process of scribe_line.py (re-connect to scribed servers)'''

# setting file ? for log-category pairs....

import sys
import os
import re

APACHE_PATH_CANDIDATES = [
    '/etc/apache', '/etc/apache2', '/etc/httpd',
    '/usr/local/apache', '/usr/local/apache2', '/usr/local/apache22', '/usr/local/httpd'
    ]
APACHE_CONFIG_FILES = ['httpd.conf', 'apache.conf', 'apache2.conf']

APACHECTL_PATH = ['bin/apachectl', '/usr/sbin/apachectl', '/usr/local/sbin/apachectl']
# for apachectl -S (only for v2/v2.2)
APACHECTL_VIRTUALHOST_CONFIG_PATTERN = re.compile('.*\((/.*:\d+)\)$')

APACHE_DOCUMENTROOT_PATTERN = re.compile('^ServerRoot +\"?(.*)\"?$')
APACHE_CUSTOMLOG_PATTERN = re.compile('^\s*CustomLog +\"?([^"]*)\"?( +.*)$')
APACHE_ERRORLOG_PATTERN = re.compile('^\s*ErrorLog +\"([^"])*\"$')

def find_root_config():
    # check ServerRoot
    pass

def find_server_root(root_config_file):
    pass

def find_apachectl():
    pass

def get_config_files(apachectl):
    # do apachectl -S
    pass

def parse_logfile_path(directive):
    # normal log path, and piped log path....
    pass

def find_log_file(config_file):
    # [{'path': path, 'type': 'access'}, {'path': path, 'type': 'error'}, ...]
    pass




