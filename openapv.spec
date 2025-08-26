#
# Conditional build:
%bcond_without	static_libs	# static libraries
#
Summary:	OpenAPV: Open Advanced Professional Video codec
Summary(pl.UTF-8):	Kodek OpenAPV (Open Advanced Professional Video)
Name:		openapv
Version:	0.2.0.1
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/AcademySoftwareFoundation/openapv/releases
Source0:	https://github.com/AcademySoftwareFoundation/openapv/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	5b0e941151de8bfb44c3acb8d420614e
URL:		https://github.com/AcademySoftwareFoundation/openapv
BuildRequires:	cmake >= 3.12
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OpenAPV provides the reference implementation of the APV codec which
can be used to record professional-grade video and associated metadata
without quality degradation. OpenAPV is free and open source software
provided by BSD license.

%description -l pl.UTF-8
OpenAPV dostarcza implementację wzorcową kodeka APV, którego można
używać do zapisu obrazu w jakości profesjonalnej, bez utraty jakości,
wraz z powiązanymi metadanymi. OpenAPV jest oprogramowaniem
wolnodostępnym na licencji BSD, z otwartym kodem źródłowym.

%package devel
Summary:	Header files for OpenAPV library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki OpenAPV
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for OpenAPV library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki OpenAPV.

%package static
Summary:	Static OpenAPV library
Summary(pl.UTF-8):	Statyczna biblioteka OpenAPV
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static OpenAPV library.

%description static -l pl.UTF-8
Statyczna biblioteka OpenAPV.

%prep
%setup -q

%build
install -d build
cd build
%cmake .. \
	-DCMAKE_INSTALL_BINDIR=bin \
	-DCMAKE_INSTALL_LIBDIR=%{_lib} \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DOAPV_APP_STATIC_BUILD=OFF \
	%{!?with_static_libs:-DOAPV_BUILD_STATIC_LIB=OFF}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc LICENSE README.md
%attr(755,root,root) %{_bindir}/oapv_app_dec
%attr(755,root,root) %{_bindir}/oapv_app_enc
%attr(755,root,root) %{_libdir}/liboapv.so.*.*.*
%ghost %{_libdir}/liboapv.so.2

%files devel
%defattr(644,root,root,755)
%{_libdir}/liboapv.so
%{_includedir}/oapv
%{_pkgconfigdir}/oapv.pc

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%dir %{_libdir}/oapv
%{_libdir}/oapv/liboapv.a
%endif
