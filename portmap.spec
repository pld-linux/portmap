Summary:     RPC port mapper
Summary(pl): Portmapper RPC 
Name:        portmap
Version:     4.0
Release:     13
Group:       Networking/Daemons
Copyright:   BSD
Source0:     ftp://coast.cs.purdue.edu/pub/tools/unix/portmap/%{name}_4.tar.gz
Source1:     %{name}.init
Patch0:      %{name}-patch
Prereq:      /sbin/chkconfig
BuildRoot:   /tmp/%{name}-%{version}-root

%description
The portmapper manages RPC connections, which are used by protocols
such as NFS and NIS. The portmap server must be running on machines
which act as servers for protocols which make use of the RPC mechanism.
This portmapper supports hosts.{allow,deny} type access control.

%description -l pl
Portmapper zarz±dca po³±czeniami RPC, z których korzystaj± protoko³y NFS
i NIS. Serwery tych protoko³ów potrzebuj± uruchomionego portmappera.
Ta wersja portmappera korzysta z plików hosts.{allow,deny} do
kontroli dostêpu.

%prep 
%setup -q -n portmap_4
%patch0 -p0 -b .glibc

%build
make FACILITY=LOG_AUTH ZOMBIES='-DIGNORE_SIGCHLD -Dlint' 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/usr/sbin
install -d $RPM_BUILD_ROOT/etc/rc.d/init.d

install -s pmap_dump pmap_set portmap $RPM_BUILD_ROOT/usr/sbin
install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portmap

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add portmap

%postun
if [ $1 = 0 ] ; then
  /sbin/chkconfig --del portmap
fi

%files
%defattr(644, root, root, 755)
%doc README CHANGES BLURB
%attr(700, root, root) %config /etc/rc.d/init.d/portmap
%attr(700, root, root) /usr/sbin/*

%changelog
* Tue Sep 29 1998 Marcin Korzonek <mkorz@shadow.eu.org>
  [4.0-13]
- added pl translation,
- defined files permission,
- some minor changes.

* Mon May 04 1998 Cristian Gafton <gafton@redhat.com>
- fixed the trigger script

* Fri May 01 1998 Jeff Johnson <jbj@redhat.com>
- added triggerpostun

* Fri May 01 1998 Cristian Gafton <gafton@redhat.com>
- added %trigger to fix a previously broken package

* Thu Apr 23 1998 Michael K. Johnson <johnsonm@redhat.com>
- enhanced initscripts

* Thu Jan 08 1998 Erik Troan <ewt@redhat.com>
- rebuilt against glibc 2.0.6

* Tue Oct 28 1997 Erik Troan <ewt@redhat.com>
- fixed service name in stop section of init script

* Tue Oct 21 1997 Donnie Barnes <djb@redhat.com>
- fixed chkconfig support

* Sun Oct 19 1997 Erik Troan <ewt@redhat.com>
- added restart, status commands to init script
- added chkconfig support
- uses a buildroot and %attr tags

* Fri Jul 18 1997 Erik Troan <ewt@redhat.com>
- built against glibc
