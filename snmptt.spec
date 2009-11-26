Name:           snmptt
Version:        1.3
Release:        %mkrel 1
Summary:        SNMP Trap Translator
Group:          System/Servers
License:        GPL
URL:            http://snmptt.sourceforge.net/
Source0:        http://sourceforge.net/projects/snmptt/files/snmptt/snmptt_%{version}/snmptt_%{version}.tgz
BuildArch:		noarch
BuildRoot:      %{_tmppath}/%{name}-%{version}

%description
SNMPTT (SNMP Trap Translator) is an SNMP trap handler written in Perl for use
with the Net-SNMP / UCD-SNMP snmptrapd program (www.net-snmp.org).

%prep
%setup -q -n %{name}_%{version}

%install
rm -rf %{buildroot}

install -d -m 755 %{buildroot}%{_sbindir}
install -m 755 snmptt snmpttconvert snmpttconvertmib snmptthandler \
    %{buildroot}%{_sbindir}
 
install -d -m 755 %{buildroot}%{_sysconfdir}/snmp
install -m 644 snmptt.ini %{buildroot}%{_sysconfdir}/snmp
install -m 644 examples/snmptt.conf.generic \
    %{buildroot}%{_sysconfdir}/snmp/snmptt.conf

install -d -m 755 %{buildroot}%{_initrddir}
install -m 755 snmptt-init.d %{buildroot}%{_initrddir}/snmptt

install -d -m 755 %{buildroot}%{_sysconfdir}/logrotate.d
cat > %{buildroot}%{_sysconfdir}/logrotate.d/snmptt <<EOF
/var/log/snmptt/*.log /var/log/snmptt/*.debug {
   sharedscripts
   postrotate
       /etc/init.d/snmptt restart > /dev/null
   endscript
}
EOF

install -d -m 755 %{buildroot}%{_localstatedir}/log/snmptt
install -d -m 755 %{buildroot}%{_localstatedir}/spool/snmptt

%clean
rm -rf %{buildroot}

%pre
%_pre_useradd %{name} %{_localstatedir}/spool/%{name} /bin/sh

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%postun
%_postun_userdel %{name}

%files
%defattr(-,root,root)
%doc BUGS ChangeLog COPYING INSTALL README
%doc docs/*html docs/*.css examples
%{_initrddir}/snmptt
%config(noreplace) %{_sysconfdir}/snmp
%config(noreplace) %{_sysconfdir}/logrotate.d/snmptt
%{_sbindir}/snmptt
%{_sbindir}/snmpttconvert
%{_sbindir}/snmpttconvertmib
%{_sbindir}/snmptthandler
%attr(-,snmptt,snmptt) %{_localstatedir}/log/snmptt
%attr(-,snmptt,snmptt) %{_localstatedir}/spool/snmptt

