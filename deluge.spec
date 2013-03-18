# Use system or static libtorrent(-rasterbar)?
%define sys_libtorrent	1
%define _enable_debug_packages %nil
%define debug_package %nil

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	1.3.6
Release:	1
License:	GPLv3+ with exceptions
Group:		Networking/File transfer
Url:		http://deluge-torrent.org/
Source0:	http://download.deluge-torrent.org/source/%{name}-%{version}.tar.bz2
# (Debian) add patch to disable checking for updates by default
Patch0:		new_release_check.patch
Patch1:		deluge-1.1.8-use-multithreaded-boost.patch
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	boost-devel
BuildRequires:	zlib-devel
BuildRequires:	openssl-devel
BuildRequires:	imagemagick
BuildRequires:	python-setuptools
BuildRequires:	intltool
%if %{sys_libtorrent}
BuildRequires:	python-libtorrent-rasterbar >= 0.14.9
%endif
Requires:	librsvg2
Requires:	pyxdg
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gnomevfs
Requires:	python-twisted-web
Requires:	python-simplejson
Requires:	python-notify
Requires:	python-OpenSSL
Requires:	python-chardet
Requires:	python-pkg-resources
%if %{sys_libtorrent}
Requires:	python-libtorrent-rasterbar >= 0.14.9
BuildArch:	noarch
%endif

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%prep
%setup -q

%patch0 -p1 -b .update
%patch1 -p1 -b .mt

%build
%ifarch x86_64 sparc64
	CFLAGS="%{optflags} -DAMD64" python setup.py build
%else
	CFLAGS="%{optflags}" python setup.py build
%endif

%install
python ./setup.py install -O1 --skip-build --root=%{buildroot}

perl -pi -e 's,%{name}.png,%{name},g' %{buildroot}%{_datadir}/applications/%{name}.desktop
mv %{buildroot}%{_iconsdir}/scalable %{buildroot}%{_iconsdir}/hicolor/

%files
%doc ChangeLog
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%if %{sys_libtorrent}
%{py_puresitedir}/*
%else
%{py_platsitedir}/*
%endif
%{_datadir}/pixmaps/%{name}.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}*.1.*


