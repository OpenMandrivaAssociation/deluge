%define name 	deluge
%define version	0.5.5
%define release	%mkrel 3
# needed to run numerical comparisons on python version
%define my_py_ver %(echo %py_ver | tr -d '.')

Summary:	Bittorrent client based on GTK+ 2
Name:		%{name}
Version:	%{version}
Release:	%{release}
Source0:	http://download.deluge-torrent.org/stable/%{name}-%{version}.tar.gz

# FOR SYSTEM LIBTORRENT Source1: %{name}-fixed-setup.py

# use renamed mt versions of boost libs
Patch0:		deluge-0.5.5-boost.patch
# Disables the automatic check for a newer version. We don't want it.
Patch1:		deluge-0.5.4.1-versioncheck.patch
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
Requires:	pyxdg
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gnomevfs

%description
Deluge is a Bittorrent client written in Python and GTK+. Deluge is 
intended to bring a native, full-featured client to Linux GTK+ desktop 
environments such as GNOME and XFCE.

%prep
%setup -q
# French translation doesn't work, causes Deluge to crash on startup
# Can't figure out why so let's remove it for now
rm -f po/fr.po
# FOR SYSTEM LIBTORRENT install -m 0755 %{SOURCE1} ./setup.py
%patch0 -p1 -b .boost
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
desktop-file-install --vendor="" \
  --add-category="GTK" \
  --remove-category="Application" \
  --add-category="P2P" \
  --add-category="FileTransfer" \
  --dir %{buildroot}%{_datadir}/applications \
%{buildroot}%{_datadir}/applications/*

# There's a method to this madness: use upstream sizes where they
# exist, for useful sizes that don't exist, convert from an upstream
# size that's an exact multiple.
for i in 22 32 48 128 192 256; do install -m 644 -D pixmaps/%{name}$i.png %{buildroot}%{_iconsdir}/hicolor/"$i"x"$i"/apps/%{name}.png; done
mkdir -p %{buildroot}%{_iconsdir}/hicolor/16x16/apps
convert -scale 16 pixmaps/%{name}32.png %{buildroot}%{_iconsdir}/hicolor/16x16/apps/%{name}.png
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
%{_iconsdir}/hicolor/*/apps/%{name}.png
