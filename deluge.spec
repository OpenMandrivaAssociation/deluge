%define debug_package %nil

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	2.1.1
Release:	4
License:	GPLv3+ with exceptions
Group:		Networking/File transfer
Url:		https://deluge-torrent.org/
Source0:	https://download.deluge-torrent.org/source/%{name}-%{version}.tar.gz
Patch0:		deluge-2.1.1-dont_check_for_new_release.patch

BuildRequires:	appstream-util
BuildRequires:	desktop-file-utils
BuildRequires:	boost-devel
BuildRequires:	imagemagick
BuildRequires:	intltool
BuildRequires:	pkgconfig(openssl)
BuildRequires:	pkgconfig(python)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(libtorrent)
BuildRequires:	python%{pyver}dist(setproctitle)
BuildRequires:	python%{pyver}dist(setuptools)
BuildRequires:	zlib-devel

Requires:	%{_lib}rsvg2_2
Requires:	python%{pyver}dist(service-identity)
Requires:	python%{pyver}dist(dbus-python)

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%files
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%{_datadir}/pixmaps/%{name}.*
%{_datadir}/appdata/%{name}.appdata.xml
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_iconsdir}/hicolor/*x*/apps/deluge-panel.png
%{_mandir}/man1/%{name}*.1.*
%{python_sitelib}/%{name}-*.*-info/
%{python_sitelib}/%{name}/

#----------------------------------------------------------------------------

%prep
%autosetup -p1

%build
%py_build

%install
%py_install

# .desktop
install -pm 0755 -d %{buildroot}%{_datadir}/applications/
desktop-file-install \
	--dir %{buildroot}%{_datadir}/applications \
	deluge/ui/data/share/applications/%{name}.desktop

# appdata
install -pm 0755 -d %{buildroot}%{_datadir}/appdata
install -pm 0644 deluge/ui/data/share/appdata/%{name}.appdata.xml %{buildroot}%{_datadir}/appdata/

