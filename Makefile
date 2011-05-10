PACKAGE = scribeline
PACKAGE_DIR = scribe_line

PREFIX ?= /usr/local
ETCDIR ?= /etc
INITDIR ?= /etc/init.d

INSTALLDIR ?= $(PREFIX)/$(PACKAGE_DIR)

all: build

build:
	echo "nothing to build."

install:
	test -d $(INSTALLDIR) || mkdir $(INSTALLDIR)
	cp -r scribe_line.sh scribe_line.py thrift fb303 scribe $(INSTALLDIR)
	chmod +x $(INSTALLDIR)/scribe_line.*
	cp package/scribeline.conf $(ETCDIR)
	cp package/scribeline $(INITDIR)
	chmod +x $(INITDIR)/scribeline
