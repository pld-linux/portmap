Summary:	RPC port mapper
Summary(pl):	Portmapper RPC 
Name:		portmap
Version:	4.0
Release:	16
Group:		Daemons
Group(pl):	Serwery
Copyright:	BSD
Source0:	ftp://coast.cs.purdue.edu/pub/tools/unix/portmap/%{name}_4.tar.gz
Source1:	portmap.init
Source2:	pmap_dump.8
Source3:	pmap_set.8
Source4:	portmap.8
Patch0:		portmap.patch
Prereq:		/sbin/chkconfig
BuildPrereq:	libwrap
BuildRoot:	/tmp/%{name}-%{version}-root

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
install -d $RPM_BUILD_ROOT/{usr/{sbin,man/man8},etc/rc.d/init.d}

install -s pmap_dump pmap_set portmap $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portmap
install %{SOURCE2} %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8

gzip -9nf $RPM_BUILD_ROOT%{_mandir}/man8/* \
	README CHANGES BLURB

%post
/sbin/chkconfig --add portmap
if test -r /var/run/portmap.pid; then
	/etc/rc.d/init.d/portmap stop >&2
	/etc/rc.d/init.d/portmap start >&2
else
	echo "Run \"/etc/rc.d/init.d/portmap start\" to start portmap daemon."
fi

%preun
if [ "$1" = "0" ] ; then
	/sbin/chkconfig --del portmap
	/etc/rc.d/init.d/portmap stop >&2
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc {README,CHANGES,BLURB}.gz

%attr(754,root,root) /etc/rc.d/init.d/portmap
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*

%changelog
* Wed Apr 21 1999 Tomasz K³oczko <kloczek@rudy.mif.pg.gda.pl>
  [4.0-16]
- added pmap_dump(8), pmap_set(8), portmap(8) man pages,
- modifications %post, %preun for standarizing this section; this allow stop
  service on uninstall and automatic restart on upgrade,
- removed %config from /etc/rc.d/init.d/portmap,
- 754 on /etc/rc.d/init.d/portmap.

* Wed Apr 21 1999 Piotr Czerwiñski <pius@pld.org.pl>
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
