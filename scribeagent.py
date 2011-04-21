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

# このスクリプトは捨てられました

'''scribeagent.py: start-stop script for scribe_line.sh.
   find httpd log scripts from config files, and send all of them with scribe_line.sh

[USAGE] scribeagent [start|stop|restart|reload|status]
  reload: send SIGHUP to all process of scribe_line.py (re-connect to scribed servers)'''

# setting file ? for log-category pairs....

import sys
import os
import os.path
import re

APACHE_PATH_CANDIDATES = [
    '/etc/apache', '/etc/apache2', '/etc/httpd',
    '/usr/local/apache', '/usr/local/apache2', '/usr/local/apache22', '/usr/local/httpd'
    ]
APACHE_CONFIG_FILES = [
    'httpd.conf', 'apache.conf', 'apache2.conf',
    'conf/httpd.conf', 'conf/apache.conf', 'conf/apache2.conf'
    ]
APACHECTL_PATH = ['bin/apachectl', '/usr/sbin/apachectl', '/usr/local/sbin/apachectl']
# for apachectl -S (only for v2/v2.2)
APACHECTL_VIRTUALHOST_CONFIG_PATTERN = re.compile('.*\((/.*:\d+)\)$')

APACHE_DOCUMENTROOT_PATTERN = re.compile('^ServerRoot +\"?(.*)\"?$')
APACHE_CUSTOMLOG_PATTERN = re.compile('^\s*CustomLog +\"?([^"]*)\"?( +.*)$')
APACHE_ERRORLOG_PATTERN = re.compile('^\s*ErrorLog +\"([^"])*\"$')

# 1. Apacheが動いてるかを ps auxww から適当にgrepして確認
#   modperlを抜くのを忘れないこと
# 2. APACHE_PATH_CANDIDATES x APACHE_CONFIG_FILES をぜんぶ探しまわる
#  2a. 見付けたら全行を読んで ServerRoot と CustomLog と ErrorLog を探す
#  2b. かつ Include があって未知であれば読むリストに追加する
# 3. APACHE_PATH_CANDIDATES x APACHETHCTL_PATH を探しまわる
#  3a. 見付けて実行可能だったら -S を実行して、見付かったVH設定が既知かどうか調べる
#  3b. 未知だったら読んで CustomLog と ErrorLog を探す

def check_apache_works():
    apache_pattern = re.compile('httpd|apache')
    reject_pattern = re.compile('mod_?perl|grep|hadoop')
    fileio = os.popen(['ps', 'auxww'])
    for line in fileio:
        cmd = ' '.join(line.split()[11:]) # get command list only
        if apache_pattern.search(cmd) and not reject_pattern.search(cmd):
            cmd_elements = filter(lambda x: '/' in x, cmd.split()) # this is for path includes space
            if len(cmd_elements) < 1:
                cmd_elements = [cmd.split()[0]]
            executed_file_name = ' '.join(cmd_elements).split('/')[-1]
            if executed_file_name in ['httpd', 'apache', 'apache2', 'apache22']:
                return True


def find_root_config():
    dirs = filter(lambda p: os.path.exists(p) and os.path.isdir(p), APACHE_PATH_CANDIDATES)
    return filter(lambda: x: os.path.exists(x) and os.path.isfile(x), [p+'/'+c for p in dirs for c in APACHE_CONFIG_FILES])


def get_server_root(root_config_file):

    # check ServerRoot from config
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




