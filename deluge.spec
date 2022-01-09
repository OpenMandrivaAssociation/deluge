# Use system or static libtorrent(-rasterbar)?
%define sys_libtorrent 1
%define _enable_debug_packages %nil
%define debug_package %nil

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	2.0.5
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
BuildRequires:	python-devel
BuildRequires:	python-wheel
%if %{sys_libtorrent}
BuildRequires:	python-libtorrent-rasterbar
%endif

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%files
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}*.1.*

#----------------------------------------------------------------------------

%prep
%setup -q

%build
%py_build

%install
%py_install
