# needed to run numerical comparisons on python version
%define my_py_ver %(echo %py_ver | tr -d '.')

Summary:	Bittorrent client based on GTK+ 2
Name:		deluge
Version:	0.5.9.0
Release:	%mkrel 1
Source0:	http://download.deluge-torrent.org/tarball/%{version}/%{name}-%{version}.tar.gz
# FOR SYSTEM LIBTORRENT Source1: %{name}-fixed-setup.py
# Disables the automatic check for a newer version. We don't want it.
Patch1:		deluge-0.5.8.4-versioncheck.patch
License:	GPLv2+
Group:		Networking/File transfer
Url:		http://deluge-torrent.org/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
BuildRequires:	desktop-file-utils
# FOR SYSTEM LIBTORRENT BuildRequires: libtorrent-rasterbar-devel
BuildRequires:	python-devel
BuildRequires:	boost-devel
BuildRequires:	libz-devel
BuildRequires:	openssl-devel
BuildRequires:	ImageMagick
Requires:	python-dbus
Requires:	librsvg2
Requires:	pyxdg
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gnomevfs

%description
Deluge is a Bittorrent client written in Python and GTK+. Deluge is 
intended to bring a native, full-featured client to Linux GTK+ desktop 
environments such as GNOME and XFCE.

%prep
%setup -q -n deluge-torrent-%version
# FOR SYSTEM LIBTORRENT install -m 0755 %{SOURCE1} ./setup.py
%patch1 -p1 -b .versioncheck

%build
# FOR SYSTEM LIBTORRENT # We forcibly don't store the installation directory during the build, so
# FOR SYSTEM LIBTORRENT # we need to ensure that it is properly inserted into the code as required.
# FOR SYSTEM LIBTORRENT perl -pi -e "s,INSTALL_PREFIX = '@datadir@',INSTALL_PREFIX = '%{_prefix}',g" \
# FOR SYSTEM LIBTORRENT 	src/dcommon.py

%ifarch x86_64 sparc64
	CFLAGS="%{optflags} -DAMD64" python setup.py build
%else
	CFLAGS="%{optflags}" python setup.py build
%endif

%install
rm -rf %{buildroot}
python ./setup.py install --root=%{buildroot}

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/%{name}.desktop
desktop-file-install \
  --add-category="GTK" \
  --remove-category="Application" \
  --add-category="P2P" \
  --add-category="FileTransfer" \
  --dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*


mkdir -p %{buildroot}%{_iconsdir}/hicolor/{48x48,32x32,16x16,scalable}/apps
install -m 644 pixmaps/%{name}.svg %{buildroot}%{_iconsdir}/hicolor/scalable/apps/%{name}.svg
install -m 644 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/48x48/apps/%{name}.png
convert -scale 32 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/32x32/apps/%{name}.png
convert -scale 16 pixmaps/%{name}.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
rm -f %{buildroot}%{_datadir}/pixmaps/%{name}.xpm

%find_lang %{name}

%post
%{update_icon_cache hicolor}
%{update_menus}
%{update_desktop_database}
%postun
%{clean_icon_cache hicolor}
%{clean_menus}
%{clean_desktop_database}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop
%if %{my_py_ver} >= 25
%{py_platsitedir}/deluge-%{version}-py*
%endif
%{py_platsitedir}/%{name}
%{_datadir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.*
