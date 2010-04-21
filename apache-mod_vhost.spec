Summary:	DSO module for the apache web server
Name:		apache-mod_vhost
Version:	2.3.1
Release:	%mkrel 13
Group:		System/Servers
License:	GPL
URL:		http://kwiatek.eu.org/mod_vhost/
# there is no official tar ball
Source0:	http://kwiatek.eu.org/mod_vhost/vhost/ver2.3.1/mod_vhost.c
Source1:	A75_mod_vhost_ldap.conf
Source2:	A76_mod_vhost_mysql1.conf
Source3:	A77_mod_vhost_pgsql.conf
Source4:	A78_mod_vhost_sqlite3.conf
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
BuildRequires:	apache-devel >= 2.2.0
BuildRequires:	file
BuildRequires:	mysql-devel
BuildRequires:	db4-devel
BuildRequires:	sqlite3-devel
BuildRequires:	postgresql-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This module is provided for Virtual Host based on LDAP Directory Server, MySQL,
PostgreSQL or SQLite3 databases. The core of this module is Berkely DB database
where are stored positive hits in LDAP/MySQL/PGSQL/SQLite3. Without this cache
probably our LDAP/MySQL/PGSQL/SQLite3 database will have problem with
productivity. First lookup is done in cache. When the hostname (Vhost from 
HTTP/1.1 Request) is not found in cache, the module search in 
LDAP/MySQL/PGSQL/SQLite3. If the entry exist in LDAP/PGSQL, module insert
values into cache, and proceed request. When there are no such entry, the
module return DECLINED, and the request is directed to DocumentRoot of the
Server.

This source rpm package will provide separate subpackages for each database
backend, like so:

 o apache-mod_vhost_ldap	- OpenLDAP support
 o apache-mod_vhost_mysql1	- MySQL support
 o apache-mod_vhost_pgsql	- PostgreSQL support
 o apache-mod_vhost_sqlite3	- SQLite3 support

%package -n	apache-mod_vhost_ldap
Summary:	This module provides Virtual Hosting based on OpenLDAP database
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Conflicts:	apache-mod_vhost_mysql
Conflicts:	apache-mod_vhost_mysql1
Conflicts:	apache-mod_vhost_pgsql
Conflicts:	apache-mod_vhost_sqlite3

%description -n	apache-mod_vhost_ldap
This module provides Virtual Hosting based on OpenLDAP database.

%package -n	apache-mod_vhost_mysql1
Summary:	This module provides Virtual Hosting based on MySQL database
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Conflicts:	apache-mod_vhost_mysql
Conflicts:	apache-mod_vhost_ldap
Conflicts:	apache-mod_vhost_pgsql
Conflicts:	apache-mod_vhost_sqlite3

%description -n	apache-mod_vhost_mysql1
This module provides Virtual Hosting based on MySQL database.

%package -n	apache-mod_vhost_pgsql
Summary:	This module provides Virtual Hosting based on PostgreSQL database
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Conflicts:	apache-mod_vhost_mysql
Conflicts:	apache-mod_vhost_mysql1
Conflicts:	apache-mod_vhost_ldap
Conflicts:	apache-mod_vhost_sqlite3

%description -n	apache-mod_vhost_pgsql
This module provides Virtual Hosting based on PostgreSQL database.

%package -n	apache-mod_vhost_sqlite3
Summary:	This module provides Virtual Hosting based on SQLite3 database
Group:		System/Servers
Requires(pre): rpm-helper
Requires(postun): rpm-helper
Requires(pre):	apache-conf >= 2.2.0
Requires(pre):	apache >= 2.2.0
Requires:	apache-conf >= 2.2.0
Requires:	apache >= 2.2.0
Conflicts:	apache-mod_vhost_mysql
Conflicts:	apache-mod_vhost_mysql1
Conflicts:	apache-mod_vhost_ldap
Conflicts:	apache-mod_vhost_pgsql

%description -n	apache-mod_vhost_sqlite3
This module provides Virtual Hosting based on SQLite3 database.

%prep

%setup -q -c -T -n mod_vhost-%{version}

cp %{SOURCE0} mod_vhost.c
cp %{SOURCE1} A75_mod_vhost_ldap.conf
cp %{SOURCE2} A76_mod_vhost_mysql1.conf
cp %{SOURCE3} A77_mod_vhost_pgsql.conf
cp %{SOURCE4} A78_mod_vhost_sqlite3.conf

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# use latest db4
perl -pi -e "s|\<db43\/db\.h\>|\<db4\/db\.h\>|g" mod_vhost.c

%build

# fix a different module for each backend

# SQLite3
cp mod_vhost.c mod_vhost_sqlite3.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_sqlite3\.c|g" mod_vhost_sqlite3.c
perl -pi -e "s|mod_vhost_module|vhost_sqlite3_module|g" mod_vhost_sqlite3.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_sqlite3/positive\.db|g" mod_vhost_sqlite3.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_sqlite3/negative\.db|g" mod_vhost_sqlite3.c
perl -pi -e "s|/tmp/baza\.db|/var/lib/apache-mod_vhost_sqlite3/baza\.db|g" mod_vhost_sqlite3.c
%{_sbindir}/apxs -DHAVE_SQLITE  -DHAVE_PHP -I%{_includedir}/pgsql -L%{_libdir} -Wl,-ldb -Wl,-lsqlite3 -c mod_vhost_sqlite3.c
mv .libs/mod_vhost_sqlite3.so .
rm -rf .libs *.{la,lo,o,slo}

# PostgreSQL
cp mod_vhost.c mod_vhost_pgsql.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_pgsql\.c|g" mod_vhost_pgsql.c
perl -pi -e "s|mod_vhost_module|vhost_pgsql_module|g" mod_vhost_pgsql.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_pgsql/positive\.db|g" mod_vhost_pgsql.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_pgsql/negative\.db|g" mod_vhost_pgsql.c
%{_sbindir}/apxs -DHAVE_PGSQL -DHAVE_PHP -I%{_includedir}/pgsql -L%{_libdir} -Wl,-ldb -Wl,-lpq -c mod_vhost_pgsql.c
mv .libs/mod_vhost_pgsql.so .
rm -rf .libs *.{la,lo,o,slo}

# MySQL
cp mod_vhost.c mod_vhost_mysql1.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_mysql1\.c|g" mod_vhost_mysql1.c
perl -pi -e "s|mod_vhost_module|vhost_mysql1_module|g" mod_vhost_mysql1.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_mysql/positive\.db|g" mod_vhost_mysql1.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_mysql/negative\.db|g" mod_vhost_mysql1.c
%{_sbindir}/apxs -DHAVE_MYSQL -DHAVE_PHP -I%{_includedir}/mysql -L%{_libdir} -Wl,-ldb -Wl,-lmysqlclient -c mod_vhost_mysql1.c
mv .libs/mod_vhost_mysql1.so .
rm -rf .libs *.{la,lo,o,slo}

# OpenLDAP
cp mod_vhost.c mod_vhost_ldap.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_ldap\.c|g" mod_vhost_ldap.c
perl -pi -e "s|mod_vhost_module|vhost_ldap_module|g" mod_vhost_ldap.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_ldap/positive\.db|g" mod_vhost_ldap.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_ldap/negative\.db|g" mod_vhost_ldap.c
%{_sbindir}/apxs -DHAVE_LDAP -DHAVE_PHP -I%{_includedir}/ldap -L%{_libdir} -Wl,-ldb -Wl,-lldap -c mod_vhost_ldap.c
mv .libs/mod_vhost_ldap.so .
rm -rf .libs *.{la,lo,o,slo}

%install
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/httpd/modules.d
install -d %{buildroot}%{_libdir}/apache-extramodules
install -d %{buildroot}/var/lib/apache-mod_vhost_sqlite3
install -d %{buildroot}/var/lib/apache-mod_vhost_pgsql
install -d %{buildroot}/var/lib/apache-mod_vhost_mysql
install -d %{buildroot}/var/lib/apache-mod_vhost_ldap

install -m0755 mod_vhost_ldap.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0755 mod_vhost_mysql1.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0755 mod_vhost_pgsql.so %{buildroot}%{_libdir}/apache-extramodules/
install -m0755 mod_vhost_sqlite3.so %{buildroot}%{_libdir}/apache-extramodules/

install -m0640 A75_mod_vhost_ldap.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/
install -m0640 A76_mod_vhost_mysql1.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/
install -m0640 A77_mod_vhost_pgsql.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/
install -m0640 A78_mod_vhost_sqlite3.conf %{buildroot}%{_sysconfdir}/httpd/modules.d/

%post -n apache-mod_vhost_ldap
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_vhost_ldap
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%post -n apache-mod_vhost_mysql1
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_vhost_mysql1
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%post -n apache-mod_vhost_pgsql
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_vhost_pgsql
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%post -n apache-mod_vhost_sqlite3
if [ -f %{_var}/lock/subsys/httpd ]; then
 %{_initrddir}/httpd restart 1>&2;
fi

%postun -n apache-mod_vhost_sqlite3
if [ "$1" = "0" ]; then
 if [ -f %{_var}/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart 1>&2
 fi
fi

%clean
[ "%{buildroot}" != "/" ] && rm -rf %{buildroot}

%files -n apache-mod_vhost_ldap
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A75_mod_vhost_ldap.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_ldap.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_ldap

%files -n apache-mod_vhost_mysql1
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A76_mod_vhost_mysql1.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_mysql1.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_mysql

%files -n apache-mod_vhost_pgsql
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A77_mod_vhost_pgsql.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_pgsql.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_pgsql

%files -n apache-mod_vhost_sqlite3
%defattr(-,root,root)
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A78_mod_vhost_sqlite3.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_sqlite3.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_sqlite3
