Summary:	RPC port mapper
Summary(pl):	Portmapper RPC 
Name:		portmap
Version:	4.0
Release:	16
Group:		Daemons
Group(pl):	Serwery
Copyright:	BSD
URL:		ftp://coast.cs.purdue.edu/pub/tools/unix/portmap/
Source0:	%{name}_4.tar.gz
Source1:	%{name}.init
Patch0:		%{name}.patch
BuildRoot:	/tmp/%{name}-%{version}-root
Prereq:		/sbin/chkconfig

%description
The portmapper manages RPC connections, which are used by protocols
such as NFS and NIS. The portmap server must be running on machines
which act as servers for protocols which make use of the RPC mechanism.
This portmapper supports hosts.{allow,deny} type access control.

%description -l pl
Portmapper zarz±dza po³±czeniami RPC, z których korzystaj± protoko³y NFS
i NIS. Serwery tych protoko³ów potrzebuj± uruchomionego portmappera.
Ta wersja portmappera korzysta z plików hosts.{allow,deny} do
kontroli dostêpu.

%prep 
%setup -q -n %{name}_4
%patch0 -p1 

%build
make FACILITY=LOG_AUTH ZOMBIES='-DIGNORE_SIGCHLD -Dlint -w' 

%install
rm -rf $RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/{usr/sbin,etc/rc.d/init.d}

install -s pmap_dump $RPM_BUILD_ROOT/usr/sbin
install -s pmap_set $RPM_BUILD_ROOT/usr/sbin
install -s portmap $RPM_BUILD_ROOT/usr/sbin

install  %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portmap

gzip -9nf README CHANGES BLURB

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add portmap

%preun
if [ $1 = 0 ] ; then
  /sbin/chkconfig --del portmap
fi

%files
%defattr(644,root,root,755)
%doc {README,CHANGES,BLURB}.gz

%attr(750,root,root) %config /etc/rc.d/init.d/*
%attr(755,root,root) /usr/sbin/*

%changelog
* Wed Apr 21 1999 Piotr Czerwiñski <pius@pld.org.pl>
  [4.0-16]
- recompiled on rpm 3.

* Tue Sep 29 1998 Marcin Korzonek <mkorz@shadow.eu.org>
  [4.0-13d]
- translations modified for pl
- defined files permission
- some minor changes

* Sun Jun 12 1998 Wojtek ¦lusarczyk <wojtek@shadow.eu.org>
  [4.0-13]
- build against glibc-2.1.

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
