# scribeline

* http://github.com/tagomoris/scribe_line

## DESCRIPTION

'scribeline' is a log transfer agent to scribed server. Works with python (2.4 or later).

## INSTALL

On RHEL/CentOS, you can use .spec file to build rpm with your customized default config file.

### RHEL/CentOS

To build your rpm package, do 5 steps below.

1. Download (newest version) tarball, and place it on SOURCES/ .
2. Download package/scribeline.conf, and place it on SOURCES/ .
3. Fix SOURCES/package/scribeline.conf as you want (ex: default scribed server information).
4. Download SPECS/scribeline.spec, and place it on SPECS/ .
5. run 'rpmbuild -ba SPECS/scribeline.spec'

To install each RHEL/CentOS host, use yum server, or copy and rpm -i on each host.

### Other Linux or Unix-like OS

On each host, do steps below.

1. Download and extract tarball, or clone repository, and move into extracted directory.
2. Do 'make install'.

    make install

## Configure and Run

### Configuration

Configuration about scribed server and transferred log files are written in /etc/scribeline.conf.

'PRIMARY_SERVER' is always required.

'SECONDARY_SERVER' is optional. 'scribeline' has fail-over feature. If you set SECONDARY_SERVER, scribeline switches connection to SECONDARY_SERVER on downtime of PRIMARY_SERVER. 

In 'LOGS', you must specify one or more pairs of 'category'(on scribed) and log path. 'scribeline' watches log file by 'tail -F', and transfer written logs to scribed server over scribe protocol. Log rotation is processed correctly.

'PYTHONPATH' is needed on hosts without 'python' command, or python2.3 (or older) as default python command. 'scribeline' needs python 2.4 or later, so you must specify needed python path on such hosts.

### Run

With properly configured /etc/scribeline.conf and init script, you can run and stop all transfer agent as below.

    # /etc/init.d/scribeline start
    # /etc/init.d/scribeline restart
    # /etc/init.d/scribeline stop

Check configured log definitions and running processes.

    # /etc/init.d/scribeline status

And reset scribed connections of each scribeline processes. (To re-connect primary server instead of secondary server immediately after downtime.)

    # /etc/init.d/scribeline reload

To reflect change of config file, you must do 'restart'.

### Run (without init script)

You can run scribeline.sh directly without init script and config file.

    # /usr/local/scribe_line/scribe_line.sh CATEGORY LOG_FILE_PATH

In typical way, run with nohup command.

    # nohup /usr/local/scribe_line/scribe_line.sh CATEGORY LOG_FILE_PATH >> /var/log/scribeline.log &

* * * * *

## License

Copyright 2011 TAGOMORI Satoshi (tagomoris)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
