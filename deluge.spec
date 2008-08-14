# needed to run numerical comparisons on python version
%define my_py_ver %(echo %py_ver | tr -d '.')

Summary:	Bittorrent client based on GTK+ 2
Name:		deluge
Version:	0.9.06
Release:	%mkrel 1
Source0:	http://download.deluge-torrent.org/tarball/%{version}/%{name}-%{version}.tar.gz
# FOR SYSTEM LIBTORRENT Source1: %{name}-fixed-setup.py
# Disable update check by default - AdamW 2008/06
Patch0:		deluge-0.9.05-update.patch
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
BuildRequires:	python-setuptools
Requires:	python-dbus
Requires:	librsvg2
Requires:	pyxdg
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gnomevfs
Requires:	python-setuptools

%description
Deluge is a Bittorrent client written in Python and GTK+. Deluge is 
intended to bring a native, full-featured client to Linux GTK+ desktop 
environments such as GNOME and XFCE.

%prep
%setup -q -n deluge-%version
%patch0 -p1 -b .update
# FOR SYSTEM LIBTORRENT install -m 0755 %{SOURCE1} ./setup.py

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
  --add-category="P2P" \
  --add-category="FileTransfer" \
  --dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*

mv %buildroot%_iconsdir/scalable %buildroot%_iconsdir/hicolor/

%find_lang %{name}

%if %mdkversion < 200900
%post
%{update_icon_cache hicolor}
%{update_menus}
%{update_desktop_database}
%endif
%if %mdkversion < 200900
%postun
%{clean_icon_cache hicolor}
%{clean_menus}
%{clean_desktop_database}
%endif

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%if %{my_py_ver} >= 25
%{py_platsitedir}/deluge-%{version}-py*
%endif
%{py_platsitedir}/%{name}
%{_datadir}/pixmaps/%{name}.png
%{_iconsdir}/hicolor/*/apps/%{name}.*
