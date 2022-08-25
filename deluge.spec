%define _enable_debug_packages %nil
%define debug_package %nil

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	2.1.1
Release:	1
License:	GPLv3+ with exceptions
Group:		Networking/File transfer
Url:		http://deluge-torrent.org/
Source0:	http://download.deluge-torrent.org/source/%{name}-%{version}.tar.gz

BuildRequires:	desktop-file-utils
BuildRequires:	pkgconfig(python2)
BuildRequires:	boost-devel
BuildRequires:	zlib-devel
BuildRequires:	pkgconfig(openssl)
BuildRequires:	imagemagick
BuildRequires:	python3dist(setuptools)
BuildRequires:	intltool
BuildRequires:	appstream-util
BuildRequires:	pkgconfig(python)
BuildRequires:	python3dist(wheel)
BuildRequires:	python3dist(libtorrent)

Requires: python3dist(libtorrent)
Requires:	python3dist(pycairo)
Requires:	python-gobject3
Recommends:	python3dist(dbus-python)
Recommends: python3dist(mako)
Requires: %{_lib}appindicator3_1
Requires: gtk+3.0
Requires: hicolor-icon-theme
Requires: %{_lib}rsvg2_2

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%files
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_datadir}/appdata/deluge.appdata.xml
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_iconsdir}/hicolor/*x*/apps/deluge-panel.png
%{_mandir}/man1/%{name}*.1.*
%{python_sitelib}/%{name}-%{version}-py*.*.egg-info/PKG-INFO
%{python_sitelib}/%{name}-%{version}-py*.*.egg-info/
%{python_sitelib}/%{name}/
#----------------------------------------------------------------------------

%prep
%setup -q

%build
%py_build

%install
%py_install
