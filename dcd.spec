Summary:	DConnect Daemon - Hub D****ct Connect for Linux
Summary(pl):	DConnect Daemon - Hub D****ct Connecta dla Linuksa
Name:		dcd
Version:	0.0.2
Release:	1
License:	GPL v2
Group:		Networking/Daemons
Source0:	ftp://pollux.ds.pg.gda.pl/Linux/DConnect/sources/stable/%{name}-%{version}.tar.gz
Patch0:		%{name}-ac_fixes.patch
URL:		http://www.dc.ds.pg.gda.pl/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	libtool
BuildRequires:	libwrap-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This is Linux D*** Connect Hub implementation for Linux. It works in
daemon mode and utilizes threads.

%description -l pl
Pakiet zawiera Linuksow± implementacjê huba D*** Connecta, który
pracuje jako demon i u¿ywa w±tków.

%prep
%setup -q
%patch0 -p1

%build
rm -f missing
libtoolize --copy --force
aclocal
autoconf
automake -a -c -f
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/etc/{sysconfig,rc.d/init.d}

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install contrib/PLD/dcd.init $RPM_BUILD_ROOT%{_sysconfdir}/rc.d/init.d/dcd
install contrib/dcd.sysconfig $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/dcd

gzip -nf9 README BUGS AUTHORS NEWS TODO doc/*.txt

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

%files
%defattr(644,root,root,755)
%doc *.gz doc/*.gz doc/*.html
%config(noreplace) %{_sysconfdir}/dcd/dchub.conf
%config(noreplace) /etc/sysconfig/dcd
%attr(755,root,root) %{_sbindir}/dcd
%attr(754,root,root) /etc/rc.d/init.d/dcd
