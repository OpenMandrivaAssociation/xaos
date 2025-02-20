%define name	xaos
%define version	3.5
%define release %mkrel 6

%define build_aalib	1

Summary:	A real-time fractal zoomer
Name:		%{name}
Version:	%{version}
Release:	%{release}
License:	GPLv2+
Group:		Sciences/Mathematics
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	libx11-devel
BuildRequires:	libxext-devel
BuildRequires:	libgsl-devel
BuildRequires:	libpng-devel
BuildRequires:	aalib-devel
Patch0:		xaos-3.5-format-string.patch
Source0:	http://downloads.sourceforge.net/sourceforge/%{name}/%{name}-%{version}.tar.gz
Source10:	%{name}.16.xpm
Source11:	%{name}.32.xpm
Source12:	%{name}.48.xpm
URL:		https://xaos.theory.org/
Obsoletes:	XaoS < %{version}-%{release}
Provides:	XaoS = %{version}-%{release}
Obsoletes:	%{name}-svgalib < %{epoch}:%{version}-%{release}
Epoch:		1

%description
XaoS is a real-time fractal zoomer. It is highly optimized. It features an
advanced help system and nice tutorial about a lot different fractals.

This package holds the binary that runs with X11.

%package aalib
Summary: Real-time fractal zoomer, aalib package
Group: Sciences/Mathematics
Obsoletes: XaoS-aalib < %{version}-%{release}
Provides: XaoS-aalib = %{version}-%{release}

%description aalib
XaoS is a real-time fractal zoomer. It is highly optimized. It features an
advanced help system and nice tutorial about a lot different fractals.

This package holds (only) the binary that runs with aalib. (Ascii-Art)

%prep
%setup -q
%patch0 -p1 -b .strfmt

CFLAGS=$(echo %optflags | sed -e "s/-O2/-O3 -malign-double -fstrict-aliasing -ffast-math/")

%if %{build_aalib}
rm -f config.cache
%configure2_5x --without-x11-driver --with-aa-driver 
%make
mv bin/xaos ./xaos-aalib
BUILD_TAG=yes
%endif

[[ -n "$BUILD_TAG" ]] && { make clean; BUILD_TAG=""; }
rm -f config.cache
%configure2_5x --with-x11-driver --without-aa-driver
%make

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_infodir}
%makeinstall LOCALEDIR=%{buildroot}%{_datadir}/locale

%if %{build_aalib}
install -m755 xaos-aalib %{buildroot}%{_bindir}
%endif
install -m644 help/xaos.hlp %{buildroot}%{_datadir}/XaoS/catalogs

mkdir -p %{buildroot}%{_datadir}/applications
cat > %{buildroot}%{_datadir}/applications/mandriva-%{name}.desktop << EOF
[Desktop Entry]
Name=XaoS
Comment=Realtime fractal zoomer
Exec=%{name}
Icon=%{name}
Terminal=false
Type=Application
Categories=Education;Science;Math;
EOF

mkdir -p %{buildroot}%{_miconsdir}
mkdir -p %{buildroot}%{_liconsdir}
cp %{SOURCE10} %{buildroot}%{_miconsdir}/%{name}.xpm
cp %{SOURCE11} %{buildroot}%{_iconsdir}/%{name}.xpm
cp %{SOURCE12} %{buildroot}%{_liconsdir}/%{name}.xpm

%find_lang %{name}

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 200900
%{update_menus}
%endif
%_install_info xaos.info

%preun
%_remove_install_info xaos.info

%if %mdkversion < 200900
%postun
%{clean_menus}
%endif


%files -f %{name}.lang
%defattr(-,root,root,0755)
%doc NEWS AUTHORS README
%{_bindir}/xaos
%{_datadir}/XaoS
%{_mandir}/man6/*
%{_infodir}/xaos*
%{_datadir}/applications/mandriva-%{name}.desktop
%{_miconsdir}/%{name}.xpm
%{_iconsdir}/%{name}.xpm
%{_liconsdir}/%{name}.xpm

%if %{build_aalib}
%files aalib
%defattr(-,root,root,0755)
%doc COPYING 
%{_bindir}/xaos-aalib
%endif
