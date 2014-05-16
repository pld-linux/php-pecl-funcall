%define		php_name	php%{?php_suffix}
%define		subver	alpha
%define		rel		3
%define		modname	funcall
%define		status	stable
Summary:	%{modname} - Add callbacks for any function/method
Summary(pl.UTF-8):	%{modname} - odwołania dla dowolnej funkcji / metody
Name:		%{php_name}-pecl-%{modname}
Version:	0.3.0
Release:	0.%{subver}.%{rel}
License:	New BSD
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}%{subver}.tgz
# Source0-md5:	65ddff0346ed4ed4fb0e3734ccf1b7d2
URL:		http://pecl.php.net/package/funcall/
BuildRequires:	%{php_name}-devel >= 4:5.0.4
BuildRequires:	rpmbuild(macros) >= 1.650
%{?requires_php_extension}
Provides:	php(%{modname}) = %{version}
Obsoletes:	php-pecl-funcall < 0.3.0-0.alpha.2
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
mv %{modname}-%{version}%{?subver}/* .

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
