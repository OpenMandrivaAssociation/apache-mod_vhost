Summary:	DSO module for the apache web server
Name:		apache-mod_vhost
Version:	2.3.1
Release:	22
Group:		System/Servers
License:	GPL
URL:		https://kwiatek.eu.org/mod_vhost/
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
BuildRequires:	db-devel
BuildRequires:	sqlite3-devel
BuildRequires:	postgresql-devel

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
%{_bindir}/apxs -DHAVE_SQLITE  -DHAVE_PHP -I%{_includedir}/pgsql -c mod_vhost_sqlite3.c %{ldflags} -L%{_libdir} -Wl,-ldb -Wl,-lsqlite3 -Wl,-lapr-1
mv .libs/mod_vhost_sqlite3.so .
rm -rf .libs *.{la,lo,o,slo}

# PostgreSQL
cp mod_vhost.c mod_vhost_pgsql.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_pgsql\.c|g" mod_vhost_pgsql.c
perl -pi -e "s|mod_vhost_module|vhost_pgsql_module|g" mod_vhost_pgsql.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_pgsql/positive\.db|g" mod_vhost_pgsql.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_pgsql/negative\.db|g" mod_vhost_pgsql.c
%{_bindir}/apxs -DHAVE_PGSQL -DHAVE_PHP -I%{_includedir}/pgsql  -c mod_vhost_pgsql.c %{ldflags} -L%{_libdir} -Wl,-ldb -Wl,-lpq -Wl,-lapr-1
mv .libs/mod_vhost_pgsql.so .
rm -rf .libs *.{la,lo,o,slo}

# MySQL
cp mod_vhost.c mod_vhost_mysql1.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_mysql1\.c|g" mod_vhost_mysql1.c
perl -pi -e "s|mod_vhost_module|vhost_mysql1_module|g" mod_vhost_mysql1.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_mysql/positive\.db|g" mod_vhost_mysql1.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_mysql/negative\.db|g" mod_vhost_mysql1.c
%{_bindir}/apxs -DHAVE_MYSQL -DHAVE_PHP -I%{_includedir}/mysql -c mod_vhost_mysql1.c %{ldflags} -L%{_libdir} -Wl,-ldb -Wl,-lmysqlclient -Wl,-lapr-1
mv .libs/mod_vhost_mysql1.so .
rm -rf .libs *.{la,lo,o,slo}

# OpenLDAP
cp mod_vhost.c mod_vhost_ldap.c
perl -pi -e "s|mod_vhost\.c|mod_vhost_ldap\.c|g" mod_vhost_ldap.c
perl -pi -e "s|mod_vhost_module|vhost_ldap_module|g" mod_vhost_ldap.c
perl -pi -e "s|/tmp/positive\.db|/var/lib/apache-mod_vhost_ldap/positive\.db|g" mod_vhost_ldap.c
perl -pi -e "s|/tmp/negative\.db|/var/lib/apache-mod_vhost_ldap/negative\.db|g" mod_vhost_ldap.c
%{_bindir}/apxs -DHAVE_LDAP -DHAVE_PHP -I%{_includedir}/ldap -c mod_vhost_ldap.c %{ldflags} -L%{_libdir} -Wl,-ldb -Wl,-lldap  -Wl,-lapr-1
mv .libs/mod_vhost_ldap.so .
rm -rf .libs *.{la,lo,o,slo}

%install

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

%files -n apache-mod_vhost_ldap
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A75_mod_vhost_ldap.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_ldap.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_ldap

%files -n apache-mod_vhost_mysql1
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A76_mod_vhost_mysql1.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_mysql1.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_mysql

%files -n apache-mod_vhost_pgsql
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A77_mod_vhost_pgsql.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_pgsql.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_pgsql

%files -n apache-mod_vhost_sqlite3
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/httpd/modules.d/A78_mod_vhost_sqlite3.conf
%attr(0755,root,root) %{_libdir}/apache-extramodules/mod_vhost_sqlite3.so
%attr(0755,apache,apache) %dir /var/lib/apache-mod_vhost_sqlite3


%changelog
* Sat Feb 11 2012 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-21mdv2012.0
+ Revision: 773237
- rebuild

* Tue May 24 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-20
+ Revision: 678434
- mass rebuild

  + Bogdano Arendartchuk <bogdano@mandriva.com>
    - build with db 5.1 (from fwang | 2011-04-12 10:35:21 +0200)

* Thu Mar 17 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-18
+ Revision: 645772
- relink against libmysqlclient.so.18

* Sat Jan 01 2011 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-17mdv2011.0
+ Revision: 627210
- rebuilt against mysql-5.5.8 libs, again

* Thu Dec 30 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-16mdv2011.0
+ Revision: 626504
- rebuilt against mysql-5.5.8 libs

* Sun Dec 05 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-14mdv2011.0
+ Revision: 609656
- rebuilt against new libdbi

* Wed Apr 21 2010 Funda Wang <fwang@mandriva.org> 2.3.1-13mdv2010.1
+ Revision: 537583
- rebuild

* Mon Mar 08 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-12mdv2010.1
+ Revision: 516223
- rebuilt for apache-2.2.15

* Thu Feb 18 2010 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-11mdv2010.1
+ Revision: 507476
- rebuild

* Tue Jan 12 2010 Buchan Milne <bgmilne@mandriva.org> 2.3.1-10mdv2010.1
+ Revision: 490360
- Rebuild for db-4.8

* Sat Aug 01 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-9mdv2010.0
+ Revision: 406676
- rebuild

* Tue Jun 30 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-8mdv2010.0
+ Revision: 391054
- fix bdb linkage (duh!)

* Tue Jan 06 2009 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-7mdv2009.1
+ Revision: 326270
- rebuild
- rebuilt against mysql-5.1.30 libs

* Mon Jul 14 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-5mdv2009.0
+ Revision: 235120
- rebuild

* Thu Jun 05 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-4mdv2009.0
+ Revision: 215664
- fix rebuild
- hard code %%{_localstatedir}/lib to ease backports

  + Pixel <pixel@mandriva.com>
    - adapt to %%_localstatedir now being /var instead of /var/lib (#22312)

* Sun Mar 09 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-3mdv2008.1
+ Revision: 182872
- rebuild

* Mon Feb 18 2008 Thierry Vignaud <tv@mandriva.org> 2.3.1-2mdv2008.1
+ Revision: 170758
- rebuild
- fix "foobar is blabla" summary (=> "blabla") so that it looks nice in rpmdrake

* Thu Jan 03 2008 Oden Eriksson <oeriksson@mandriva.com> 2.3.1-1mdv2008.1
+ Revision: 142103
- 2.3.1
- bunzip the sources
- fix build
- rebuilt against openldap-2.4.7 libs

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Sat Sep 08 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3-5mdv2008.0
+ Revision: 82694
- rebuild


* Sat Mar 10 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3-4mdv2007.1
+ Revision: 140770
- rebuild

* Fri Jan 19 2007 Oden Eriksson <oeriksson@mandriva.com> 2.3-3mdv2007.1
+ Revision: 110745
- rebuilt against new postgresql libs

* Thu Nov 09 2006 Oden Eriksson <oeriksson@mandriva.com> 2.3-2mdv2007.0
+ Revision: 79541
- Import apache-mod_vhost

* Tue Sep 05 2006 Oden Eriksson <oeriksson@mandriva.com> 2.3-1mdv2007.0
- rebuilt against MySQL-5.0.24a-1mdv2007.0 due to ABI changes

* Sat Jul 22 2006 Oden Eriksson <oeriksson@mandriva.com> 2.3-1mdv2007.0
- initial Mandriva package

