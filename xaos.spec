%define name	xaos
%define version	3.2.3
%define release %mkrel 2

%define build_aalib	1
%define build_svgalib	1

Summary:	A real-time fractal zoomer
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sciences/Mathematics
BuildRequires: autoconf2.5 XFree86-devel libpng-devel zlib-devel aalib-devel gpm-devel ncurses-devel slang
Patch2:		XaoS-3.1pre1-64bit-fixes.patch.bz2
Patch3:		XaoS-3.1-x11shm-errors.patch.bz2
Patch4:		XaoS-3.1-xlibs-path.patch.bz2
Source0:	http://belnet.dl.sourceforge.net/sourceforge/xaos/XaoS-%{version}.tar.bz2
Source10:	%{name}.16.xpm.bz2
Source11:	%{name}.32.xpm.bz2
Source12:	%{name}.48.xpm.bz2
URL:		http://xaos.theory.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
ExclusiveArch:	%{ix86} ppc x86_64
Obsoletes:	XaoS
Provides:	XaoS = %{version}-%{release}
Epoch:		1

%description
XaoS is a real-time fractal zoomer. It is highly optimized. It features an
advanced help system and nice tutorial about a lot different fractals.

This package holds the binary that runs with X11.

%package svgalib
Summary: Real-time fractal zoomer, svgalib package
Group: Sciences/Mathematics
Obsoletes: XaoS-svgalib
Provides: XaoS-svgalib = %{version}-%{release}

%description svgalib
XaoS is a real-time fractal zoomer. It is highly optimized. It features an
advanced help system and nice tutorial about a lot different fractals.

This package holds (only) the binary that runs with svgalib.

%package aalib
Summary: Real-time fractal zoomer, aalib package
Group: Sciences/Mathematics
Obsoletes: XaoS-aalib
Provides: XaoS-aalib = %{version}-%{release}

%description aalib
XaoS is a real-time fractal zoomer. It is highly optimized. It features an
advanced help system and nice tutorial about a lot different fractals.

This package holds (only) the binary that runs with aalib. (Ascii-Art)

%prep
%setup -q -n XaoS-%{version}
%patch2 -p1 -b .64bit-fixes
%patch3 -p0 -b .x11shm-errors
%patch4 -p0 -b .xlibs-path
autoconf

%build
BUILD_TAG=""

%if %{build_aalib}
rm -f config.cache
%configure2_5x --without-x11-driver --without-ggi-driver --without-svga-driver --with-aa-driver
make
mv bin/xaos ./xaos-aalib
BUILD_TAG=yes
%endif

%if %{build_svgalib}
[[ -n "$BUILD_TAG" ]] && { make clean; BUILD_TAG=""; }
rm -f config.cache
%configure2_5x --without-x11-driver --without-ggi-driver --with-svga-driver --without-aa-driver
make
mv bin/xaos ./xaos-svgalib
BUILD_TAG=yes
%endif

[[ -n "$BUILD_TAG" ]] && { make clean; BUILD_TAG=""; }
rm -f config.cache
%configure2_5x --with-x11-driver --without-ggi-driver --without-svga-driver --without-aa-driver
make

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_infodir}
%makeinstall LOCALEDIR=$RPM_BUILD_ROOT%{_datadir}/locale

%if %{build_aalib}
install -m755 xaos-aalib $RPM_BUILD_ROOT%{_bindir}
%endif
%if %{build_svgalib}
install -m755 xaos-svgalib $RPM_BUILD_ROOT%{_bindir}
%endif
install -m644 help/xaos.hlp $RPM_BUILD_ROOT%{_datadir}/XaoS/catalogs

mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
cat > $RPM_BUILD_ROOT%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Encoding=UTF-8
Name=XaoS
Comment=Realtime fractal zoomer
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=X-MandrivaLinux-MoreApplications-Sciences-Mathematics;Science;Math;
EOF

mkdir -p $RPM_BUILD_ROOT%{_miconsdir}
mkdir -p $RPM_BUILD_ROOT%{_liconsdir}
bzcat %{SOURCE10} > $RPM_BUILD_ROOT%{_miconsdir}/%{name}.xpm
bzcat %{SOURCE11} > $RPM_BUILD_ROOT%{_iconsdir}/%{name}.xpm
bzcat %{SOURCE12} > $RPM_BUILD_ROOT%{_liconsdir}/%{name}.xpm

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{update_menus}
%_install_info xaos.info

%preun
%_remove_install_info xaos.info

%postun
%{clean_menus}


%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc COPYING TODO doc/PROBLEMS doc/README doc/README.bugs doc/compilers.txt
%{_bindir}/xaos
%{_datadir}/XaoS
%{_mandir}/man6/*
%{_infodir}/xaos*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.xpm
%{_iconsdir}/%{name}.xpm
%{_liconsdir}/%{name}.xpm

%if %{build_svgalib}
%files svgalib
%defattr(-,root,root,0755)
%doc COPYING 
%{_bindir}/xaos-svgalib
%endif

%if %{build_aalib}
%files aalib
%defattr(-,root,root,0755)
%doc COPYING 
%{_bindir}/xaos-aalib
%endif
