Summary:	DConnect Daemon - Hub D****ct Connect for Linux
Summary(pl):	DConnect Daemon - Hub D****ct Connecta dla Linuksa
Name:		dcd
Version:	0.4.7
Release:	0.1
License:	GPL v2
Group:		Networking/Daemons
Vendor:		DConnect Team <dc-hub@ds.pg.gda.pl>
Source0:	ftp://pollux.ds.pg.gda.pl/pub/Linux/DConnect/sources/stable/%{name}-%{version}.tar.bz2
# Source0-md5:	ec173dce131d71862a58575760362234
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

%triggerpostun -- dcd < 0.3.5
echo "Upgrading from version < 0.3.5"
if [ -e /etc/dcd/console.users.rpmsave ]; then
	cp /etc/dcd/dcd.users /etc/dcd/dcd.users.rpmnew
	cp /etc/dcd/console.users.rpmsave /etc/dcd/dcd.users
fi
echo "Remember to review config - console users has been changed into dcd.users"
cp /etc/dcd/dcd.conf /etc/dcd/dcd.conf.rpmsave
sed -e s/console.users/dcd.users/g /etc/dcd/dcd.conf >/etc/dcd/dcd.conf.tmp
mv -f /etc/dcd/dcd.conf.tmp /etc/dcd/dcd.conf

%files
%defattr(644,root,root,755)
%doc AUTHORS BUGS FAQ NEWS README TODO doc/*.html
%attr(755,daemon,root) %dir %{_sysconfdir}/dcd
%attr(660,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/console.allow
%attr(660,root,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.users
%attr(660,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.banned
%attr(664,daemon,daemon) %config(noreplace) %{_sysconfdir}/dcd/dcd.penalties
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
