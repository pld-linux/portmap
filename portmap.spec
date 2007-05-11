Summary:	RPC port mapper
Summary(pl.UTF-8):	Portmapper RPC
Name:		portmap
Version:	6.0
Release:	0.1
License:	BSD
Group:		Daemons
Source0:	http://neil.brown.name/portmap/%{name}-%{version}.tgz
# Source0-md5:	ac108ab68bf0f34477f8317791aaf1ff
Source1:	%{name}.init
Source2:	pmap_dump.8
Source3:	pmap_set.8
Source4:	%{name}.8
Source5:	%{name}.sysconfig
Patch0:		%{name}-pld.patch
Patch1:		%{name}-libwrap_shared.patch
Patch2:		%{name}-errno.patch
Patch3:		%{name}-misc.patch
Patch4:		%{name}-access.patch
Patch5:		%{name}-rpc_user.patch
Patch6:		%{name}-sigpipe.patch
Patch7:		%{name}-man.patch
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires:	/sbin/chkconfig
Requires:	libwrap >= 7.6-38
Requires:	rc-scripts
Provides:	user(rpc)
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The portmapper manages RPC connections, which are used by protocols
such as NFS and NIS. The portmap server must be running on machines
which act as servers for protocols which make use of the RPC
mechanism. This portmapper supports hosts.{allow,deny} type access
control.

%description -l es.UTF-8
portmap administra conexiones RPC, que incluye NFS. Este mapeador de
puerto puede usar hosts.{allow,deny} para controlar el acceso.

%description -l pl.UTF-8
Portmapper zarządza połączeniami RPC, z których korzystają protokoły
NFS i NIS. Serwery tych protokołów potrzebują uruchomionego
portmappera. Ta wersja portmappera korzysta z plików
hosts.{allow,deny} do kontroli dostępu.

%description -l pt_BR.UTF-8
O portmap gerencia conexões RPC, incluindo NFS. Este mapeador de porta
pode usar hosts.{allow,deny} para controlar o acesso.

%prep
%setup -q -n %{name}_%{version}
install %{SOURCE2} %{SOURCE3} %{SOURCE4} .
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

%build
%{__make} \
	CC="%{__cc}" \
	OPT="%{rpmcflags}" \
	FACILITY=LOG_AUTH \
	AUX= \
	ZOMBIES=-DIGNORE_SIGCHLD

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sbindir},%{_mandir}/man8}
install -d $RPM_BUILD_ROOT{/var/lib/misc,/etc/{sysconfig,rc.d/init.d}}

install pmap_dump pmap_set portmap $RPM_BUILD_ROOT%{_sbindir}
install pmap_dump.8 pmap_set.8 portmap.8 $RPM_BUILD_ROOT%{_mandir}/man8

install %{SOURCE1} $RPM_BUILD_ROOT/etc/rc.d/init.d/portmap
install %{SOURCE5} $RPM_BUILD_ROOT/etc/sysconfig/portmap

touch $RPM_BUILD_ROOT/var/lib/misc/portmap.dump

%clean
rm -rf $RPM_BUILD_ROOT

%pre
%useradd -u 22 -d /usr/share/empty -s /bin/false -c "Portmapper RPC User" -g nobody rpc

%post
/sbin/chkconfig --add portmap
%service portmap restart "portmap daemon"

%preun
if [ "$1" = "0" ] ; then
	%service portmap stop
	/sbin/chkconfig --del portmap
fi

%postun
if [ "$1" = "0" ]; then
	%userremove rpc
fi

%triggerpostun -- portmap <= portmap-4.0-9
/sbin/chkconfig --add portmap

%files
%defattr(644,root,root,755)
%doc README CHANGES BLURB
%attr(754,root,root) /etc/rc.d/init.d/portmap
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/portmap
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%ghost /var/lib/misc/portmap.dump
