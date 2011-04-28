%define name scribeline
%define version 1.1
%define prefix /usr/local/scribe_line
%define _use_internal_dependency_generator 0

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')


Name:           scribeline
Version:        %{version}
Release:        original
Summary:        Log transfer agent service over scribe protocol

Group:          Applications/System
License:        Apache Software License v2
URL:            https://github.com/tagomoris/scribe_line
Source0:        https://github.com/downloads/tagomoris/scribe_line/scribeline_%{version}.tar.gz
Source1:        scribeline.conf
BuildRoot:      %{_tmppath}/%{name}-root

BuildArch:      noarch
AutoReq:        no

%description
Log transfer agent service over scribe protocol.

%prep
%setup -q -n scribe_line

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{prefix}
install -m 755 scribe_line.sh scribe_line.py scribe_cat $RPM_BUILD_ROOT%{prefix}
cp -r thrift fb303 scribe $RPM_BUILD_ROOT%{prefix}

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/init.d
install -m 644 %{Source1} $RPM_BUILD_ROOT%{_sysconfdir}/scribeline.conf
install -m 755 package/scribeline $RPM_BUILD_ROOT%{_sysconfdir}/init.d/scribeline

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{prefix}/*
%{_sysconfdir}/scribeline.conf
%{_sysconfdir}/init.d/scribeline
%doc README

%changelog
* Tue Apr 26 2011 TAGOMORI Satoshi <tagomoris@gmail.com>
- initial packaging attempt
