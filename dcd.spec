Summary:	DConnect Daemon - Hub D****ct Connect for Linux
Summary(pl):	DConnect Daemon - Hub D****ct Connecta dla Linuksa
Name:		dcd
Version:	0.6.7
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://pollux.ds.pg.gda.pl/pub/Linux/DConnect/sources/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	12437ff52683fdf3377591039f55e8e8
URL:		http://www.dc.ds.pg.gda.pl/
BuildRequires:	autoconf >= 2.52
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRequires:	rpmbuild(macros) >= 1.268
Requires(post,preun):	/sbin/chkconfig
Requires(triggerpostun):	sed >= 4.0
Requires:	rc-scripts
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is Linux D*** Connect Hub implementation for Linux. It works in
daemon mode and utilizes threads.

%description -l pl
Pakiet zawiera linuksow± implementacjê huba D*** Connecta, który
pracuje jako demon i u¿ywa w±tków.

%prep
%setup -q

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-config-dir=%{_sysconfdir}/dcd \
	--with-user=daemon \
	--with-group=daemon

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/etc/{sysconfig,rc.d/init.d,logrotate.d},/var/log/archiv/dcd}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install contrib/PLD/dcd.init $RPM_BUILD_ROOT/etc/rc.d/init.d/dcd
install contrib/dcd.sysconfig $RPM_BUILD_ROOT/etc/sysconfig/dcd
install contrib/logrotate.dcd $RPM_BUILD_ROOT/etc/logrotate.d/dcd

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add dcd
%service dcd restart "DConnect Daemon"

%preun
if [ "$1" = "0" ]; then
	%service dcd stop
	/sbin/chkconfig --del dcd
fi

%triggerpostun -- dcd < 0.3.5
echo "Upgrading from version < 0.3.5"
if [ -e /etc/dcd/console.users.rpmsave ]; then
	cp /etc/dcd/dcd.users /etc/dcd/dcd.users.rpmnew
	cp /etc/dcd/console.users.rpmsave /etc/dcd/dcd.users
fi
umask 002
echo "Remember to review config - console users has been changed into dcd.users"
cp /etc/dcd/dcd.conf /etc/dcd/dcd.conf.rpmsave
sed -i -e 's/console.users/dcd.users/g' /etc/dcd/dcd.conf

%triggerpostun -- dcd < 0.4.6
echo "Upgrading from version < 0.4.6"
sed -i -e 's/minimum_sleep_time\b/minimal_sleep_time/' /etc/dcd/dcd.conf

%triggerpostun -- dcd < 0.4.9
echo "Upgrading from version < 0.4.9"
sed -i -e 's/ping_timeout/idle_timeout/' /etc/dcd/dcd.conf

%triggerpostun -- dcd < 0.5.5
echo "Upgrading from version < 0.5.5"
sed -i -e 's/listen_interface/bind_address/' /etc/dcd/dcd.conf

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS FAQ NEWS README TODO
%attr(755,daemon,root) %dir %{_sysconfdir}/dcd
%attr(660,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/console.allow
%attr(660,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.users
%attr(660,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.banned
%attr(664,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.penalties
%attr(664,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.conf
%attr(664,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.motd
%attr(664,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.welcome
%attr(664,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/nicks.allow
%attr(664,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.rules
%config(noreplace) %verify(not md5 mtime size) /etc/sysconfig/dcd
%config(noreplace) /etc/logrotate.d/dcd
%attr(755,root,root) %{_sbindir}/dcd
%attr(755,root,root) %{_sbindir}/dcd.adduser
%attr(754,root,root) /etc/rc.d/init.d/dcd
%attr(751,daemon,root) %dir /var/log/dcd
%attr(751,daemon,root) %dir /var/log/archiv/dcd
%{_mandir}/man1/*.1*
%{_mandir}/man2/*.2*
