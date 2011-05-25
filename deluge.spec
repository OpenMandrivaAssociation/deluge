# Use system or static libtorrent(-rasterbar)?
%define sys_libtorrent	1

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	1.3.2
Release:	1
License:	GPLv3+ with exceptions
Group:		Networking/File transfer
Url:		http://deluge-torrent.org/
Source0:	http://download.deluge-torrent.org/source/%{name}-%{version}.tar.lzma
# (Debian) add patch to disable checking for updates by default
Patch0:		new_release_check.patch
Patch1:		deluge-1.1.8-use-multithreaded-boost.patch
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	boost-devel
BuildRequires:	libz-devel
BuildRequires:	openssl-devel
BuildRequires:	imagemagick
BuildRequires:	python-setuptools
%if %sys_libtorrent
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
%if %mdkversion > 200900
Requires:	python-pkg-resources
%else
Requires:	python-setuptools
%endif
%if %sys_libtorrent
Requires:	python-libtorrent-rasterbar >= 0.14.9
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%prep
%setup -q -n %name-%version

%patch0 -p1 -b .update
%patch1 -p1 -b .mt

%build
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

mv %{buildroot}%{_iconsdir}/scalable %{buildroot}%{_iconsdir}/hicolor/

%find_lang %{name}

%clean
rm -rf %{buildroot}

%files -f %{name}.lang
%defattr(-,root,root)
%doc ChangeLog
%{_bindir}/%{name}*
%{_datadir}/applications/%{name}.desktop
%if sys_libtorrent
%{py_puresitedir}/*
%else
%{py_platsitedir}/*
%endif
%{_datadir}/pixmaps/%{name}.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}*.1.*
