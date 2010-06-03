%define		modname	funcall
%define		status		stable
Summary:	%{modname} - Add callbacks for any function/method
Summary(pl.UTF-8):	%{modname} - odwołania dla dowolnej funkcji / metody
Name:		php-pecl-%{modname}
Version:	0.2.5
Release:	2
License:	New BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	0c4f2a989d3b21f1dab56b9959fb9fe8
URL:		http://pecl.php.net/package/funcall/
BuildRequires:	php-devel >= 4:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.344
%{?requires_php_extension}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Call callbacks before or after specified functions/methods being
called.

In PECL status of this extension is: %{status}.

%description -l pl.UTF-8
Rozszerzenie to pozwala na wykonywanie odwołań przed lub po wywołaniu
określonej funkcji / metody.

To rozszerzenie ma w PECL status: %{status}.

%prep
%setup -qc
mv %{modname}-%{version}/* .

%build
phpize
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d

%{__make} install \
	EXTENSION_DIR=%{php_extensiondir} \
	INSTALL_ROOT=$RPM_BUILD_ROOT
cat <<'EOF' > $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini
; Enable %{modname} extension module
extension=%{modname}.so
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc TODO funcall.php
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
