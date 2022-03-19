#
# Conditional build:
%bcond_without	prof	# profiling library
#
%define		pkgname	data-default-instances-dlist
Summary:	Default instances for the type 'DList'
Summary(pl.UTF-8):	Domyślne instancje dla typu 'DList'
Name:		ghc-%{pkgname}
Version:	0.0.1
Release:	3
License:	BSD
Group:		Development/Languages
#Source0Download: http://hackage.haskell.org/package/data-default-instances-dlist
Source0:	http://hackage.haskell.org/package/%{pkgname}-%{version}/%{pkgname}-%{version}.tar.gz
# Source0-md5:	6683d943ab70b7077ff6837fce75b4de
URL:		http://hackage.haskell.org/package/data-default-instances-dlist
BuildRequires:	ghc >= 6.12.3
BuildRequires:	ghc-base >= 2
BuildRequires:	ghc-base < 5
BuildRequires:	ghc-data-default-class
BuildRequires:	ghc-dlist
%if %{with prof}
BuildRequires:	ghc-prof >= 6.12.3
BuildRequires:	ghc-base-prof >= 2
BuildRequires:	ghc-base-prof < 5
BuildRequires:	ghc-data-default-class-prof
BuildRequires:	ghc-dlist-prof
%endif
BuildRequires:	rpmbuild(macros) >= 1.608
%requires_eq	ghc
Requires:	ghc-base >= 2
Requires:	ghc-base < 5
Requires:	ghc-data-default-class
Requires:	ghc-dlist
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# debuginfo is not useful for ghc
%define		_enable_debug_packages	0

# don't compress haddock files
%define		_noautocompressdoc	*.haddock

%description
This module defines 'Default' instances for the type 'DList'.

%description -l pl.UTF-8
Ten moduł definiuje domyślne instancje ('Default') dla typu 'DList'.

%package prof
Summary:	Profiling %{pkgname} library for GHC
Summary(pl.UTF-8):	Biblioteka profilująca %{pkgname} dla GHC
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	ghc-base-prof >= 2
Requires:	ghc-base-prof < 5
Requires:	ghc-data-default-class-prof
Requires:	ghc-dlist-prof

%description prof
Profiling %{pkgname} library for GHC. Should be installed when
GHC's profiling subsystem is needed.

%description prof -l pl.UTF-8
Biblioteka profilująca %{pkgname} dla GHC. Powinna być zainstalowana
kiedy potrzebujemy systemu profilującego z GHC.

%package doc
Summary:	HTML documentation for ghc %{pkgname} package
Summary(pl.UTF-8):	Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}
Group:		Documentation

%description doc
HTML documentation for ghc %{pkgname} package.

%description doc -l pl.UTF-8
Dokumentacja w formacie HTML dla pakietu ghc %{pkgname}.

%prep
%setup -q -n %{pkgname}-%{version}

%build
runhaskell Setup.lhs configure -v2 \
	%{?with_prof:--enable-library-profiling} \
	--prefix=%{_prefix} \
	--libdir=%{_libdir} \
	--libexecdir=%{_libexecdir} \
	--docdir=%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs build
runhaskell Setup.lhs haddock --executables

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d

runhaskell Setup.lhs copy --destdir=$RPM_BUILD_ROOT

# work around automatic haddock docs installation
%{__rm} -rf %{name}-%{version}-doc
cp -a $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/html %{name}-%{version}-doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}

runhaskell Setup.lhs register \
	--gen-pkg-config=$RPM_BUILD_ROOT%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%ghc_pkg_recache

%postun
%ghc_pkg_recache

%files
%defattr(644,root,root,755)
%doc LICENSE 
%{_libdir}/%{ghcdir}/package.conf.d/%{pkgname}.conf
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdata-default-instances-dlist-%{version}-*.so
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdata-default-instances-dlist-%{version}-*.a
%exclude %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdata-default-instances-dlist-%{version}-*_p.a
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Default
%dir %{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Default/Instances
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Default/Instances/DList.hi
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Default/Instances/DList.dyn_hi

%if %{with prof}
%files prof
%defattr(644,root,root,755)
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/libHSdata-default-instances-dlist-%{version}-*_p.a
%{_libdir}/%{ghcdir}/%{pkgname}-%{version}/Data/Default/Instances/DList.p_hi
%endif

%files doc
%defattr(644,root,root,755)
%doc %{name}-%{version}-doc/*
