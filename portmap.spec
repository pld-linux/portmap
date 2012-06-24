Summary:	RPC port mapper
Summary(pl):	Portmapper RPC 
Name:		portmap
Version:	5beta
Release:	7
Group:		Daemons
Group(de):	Server
Group(pl):	Serwery
License:	BSD
Source0:	ftp://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
Source1:	%{name}.init
Source2:	pmap_dump.8
Source3:	pmap_set.8
Source4:	%{name}.8
Source5:	%{name}.sysconfig
Patch0:		%{name}-pld.patch
Patch1:		%{name}-libwrap_shared.patch
Patch2:		%{name}-malloc.patch
Patch3:		%{name}-cleanup.patch
Prereq:		/sbin/chkconfig
Prereq:		rc-scripts
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The portmapper manages RPC connections, which are used by protocols
such as NFS and NIS. The portmap server must be running on machines
which act as servers for protocols which make use of the RPC
mechanism. This portmapper supports hosts.{allow,deny} type access
control.

%description -l pl
Portmapper zarz�dza po��czeniami RPC, z kt�rych korzystaj� protoko�y
NFS i NIS. Serwery tych protoko��w potrzebuj� uruchomionego
portmappera. Ta wersja portmappera korzysta z plik�w
hosts.{allow,deny} do kontroli dost�pu.

%prep 
%setup  -q -n %{name}_5beta
%patch0 -p1 
%patch1 -p1 
%patch2 -p1 
%patch3 -p1 

%build
%{__make} OPT="%{rpmcflags}" \
	FACILITY=LOG_AUTH \
	ZOMBIES='-DIGNORE_SIGCHLD -Dlint -w' 

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8,%{_sysconfdir}/{sysconfig,rc.d/init.d}}

install pmap_dump pmap_set portmap $RPM_BUILD_ROOT%{_sbindir}

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portmap
install %{SOURCE2} %{SOURCE3} %{SOURCE4} $RPM_BUILD_ROOT%{_mandir}/man8
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/portmap

gzip -9nf README CHANGES BLURB

%post
/sbin/chkconfig --add portmap
if [ -f /var/lock/subsys/portmap ]; then
	/etc/rc.d/init.d/portmap restart >&2
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

%triggerpostun -- portmap <= portmap-4.0-9
/sbin/chkconfig --add portmap

%files
%defattr(644,root,root,755)
%doc {README,CHANGES,BLURB}.gz

%attr(754,root,root) /etc/rc.d/init.d/portmap
%attr(640,root,root) %config %verify(not size mtime md5) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
