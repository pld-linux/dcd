Summary:	DConnect Daemon - Hub D****ct Connect for Linux
Summary(pl):	DConnect Daemon - Hub D****ct Connecta dla Linuksa
Name:		dcd
Version:	0.2.14
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Vendor:		DConnect Team <dc-hub@ds.pg.gda.pl>
Source0:	ftp://pollux.ds.pg.gda.pl/pub/Linux/DConnect/sources/devel/%{name}-%{version}.tar.bz2
# Source0-md5:	8d43ac00305b1de3d048082c46b92207
URL:		http://www.dc.ds.pg.gda.pl/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libwrap-devel
PreReq:		rc-scripts
Requires(post,preun):	/sbin/chkconfig
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is Linux D*** Connect Hub implementation for Linux. It works in
daemon mode and utilizes threads.

%description -l pl
Pakiet zawiera Linuksow± implementacjê huba D*** Connecta, który
pracuje jako demon i u¿ywa w±tków.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--sysconfdir=%{_sysconfdir}/dcd \
	--with-user=daemon \
	--with-group=daemon

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_sysconfdir}/{sysconfig,rc.d/init.d,logrotate.d},/var/log/archiv/dcd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install contrib/PLD/dcd.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dcd
install contrib/dcd.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/dcd
install contrib/logrotate.dcd $RPM_BUILD_ROOT%{_sysconfdir}/logrotate.d/dcd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dcd
if [ -f /var/lock/subsys/dcd ]; then
	/etc/rc.d/init.d/dcd restart 1>&2
else
	echo "Run \"/etc/rc.d/init.d/dcd start\" to start DConnect Daemon."
fi

%preun
if [ "$1" = "0" ]; then
	if [ -f /var/lock/subsys/dcd ]; then
		/etc/rc.d/init.d/dcd stop 1>&2
	fi
	/sbin/chkconfig --del dcd
fi

#%triggerpostun -- dcd < 0.1.1
#echo "Upgrading from version < 0.1.1"
#echo "Remember to review config - the options were changed!!!"
#if [ -e /etc/dcd/dchub.conf.rpmsave ]; then
#	cp /etc/dcd/dchub.conf.rpmsave /etc/dcd/dcd.conf
#fi

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS FAQ NEWS README TODO doc/*.html
%attr(755,daemon,root) %dir %{_sysconfdir}/dcd
%attr(660,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/console.allow
%attr(660,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/console.users
%attr(660,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.banned
%attr(664,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.conf
%attr(664,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.motd
%attr(664,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.welcome
%attr(664,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/nicks.allow
%config(noreplace) %{_sysconfdir}/sysconfig/dcd
%config(noreplace) %{_sysconfdir}/logrotate.d/dcd
%attr(755,root,root) %{_sbindir}/dcd
%attr(754,root,root) %{_sysconfdir}/rc.d/init.d/dcd
%attr(751,daemon,root) %dir /var/log/dcd
%attr(751,daemon,root) %dir /var/log/archiv/dcd
%{_mandir}/man1/*.1*
%{_mandir}/man2/*.2*
