Summary:	RPC port mapper
Summary(pl):	Portmapper RPC
Name:		portmap
Version:	5beta
Release:	18
Group:		Daemons
License:	BSD
Source0:	ftp://ftp.porcupine.org/pub/security/%{name}_%{version}.tar.gz
# Source0-md5:	781e16ed4487c4caa082c6fef09ead4f
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
Requires(post,preun):	/sbin/chkconfig
Requires:	rc-scripts
Requires:	/sbin/chkconfig
Provides:	user(rpc)
Conflicts:	libwrap < 7.6-38
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_sbindir	/sbin

%description
The portmapper manages RPC connections, which are used by protocols
such as NFS and NIS. The portmap server must be running on machines
which act as servers for protocols which make use of the RPC
mechanism. This portmapper supports hosts.{allow,deny} type access
control.

%description -l es
portmap administra conexiones RPC, que incluye NFS. Este mapeador de
puerto puede usar hosts.{allow,deny} para controlar el acceso.

%description -l pl
Portmapper zarz±dza po³±czeniami RPC, z których korzystaj± protoko³y
NFS i NIS. Serwery tych protoko³ów potrzebuj± uruchomionego
portmappera. Ta wersja portmappera korzysta z plików
hosts.{allow,deny} do kontroli dostêpu.

%description -l pt_BR
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
if [ -f /var/lock/subsys/portmap ]; then
	/etc/rc.d/init.d/portmap restart >&2
else
	echo "Run \"/etc/rc.d/init.d/portmap start\" to start portmap daemon."
fi

%preun
if [ "$1" = "0" ] ; then
	if [ -f /var/lock/subsys/portmap ]; then
		/etc/rc.d/init.d/portmap stop >&2
	fi
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
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/*
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man8/*
%ghost /var/lib/misc/portmap.dump
