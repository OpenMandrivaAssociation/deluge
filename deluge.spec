# needed to run numerical comparisons on python version
%define my_py_ver %(echo %py_ver | tr -d '.')

# Use system or static libtorrent(-rasterbar)?
%define sys_libtorrent	1

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	1.0.7
Release:	%mkrel 2
License:	GPLv3+ with exceptions
Group:		Networking/File transfer
Url:		http://deluge-torrent.org/
Source0:	http://download.deluge-torrent.org/source/%{version}/%{name}-%{version}.tar.bz2
# Disable update check by default - AdamW 2008/06
Patch0:		deluge-0.9.05-update.patch
Patch1:		deluge-1.0.7-use-multithreaded-boost.patch
# From upstream SVN (rev 4419+4420): fix running against system
# libtorrent 0.14+ - AdamW 2008/12
Patch2:		deluge-1.0.7-libtorrent14.patch
BuildRequires:	desktop-file-utils
BuildRequires:	python-devel
BuildRequires:	boost-devel
BuildRequires:	libz-devel
BuildRequires:	openssl-devel
BuildRequires:	imagemagick
BuildRequires:	python-setuptools
%if %sys_libtorrent
BuildRequires:	python-libtorrent-rasterbar
%endif
Requires:	python-dbus
Requires:	librsvg2
Requires:	pyxdg
Requires:	pygtk2.0-libglade
Requires:	gnome-python-gnomevfs
%if %mdkversion > 200900
Requires:	python-pkg-resources
%else
Requires:	python-setuptools
%endif
%if %sys_libtorrent
Requires:	python-libtorrent-rasterbar
BuildArch:	noarch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Deluge is a Bittorrent client. Deluge is intended to bring a native,
full-featured client to Linux GTK+ desktop environments such as GNOME
and XFCE.

%prep
%setup -q
%patch0 -p1 -b .update
%patch1 -p1 -b .mt
%patch2 -p1 -b .libtorrent14

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
%{py_puresitedir}/deluge-%{version}-py*
%endif
%{py_puresitedir}/%{name}
%{_datadir}/pixmaps/%{name}.*
%{_iconsdir}/hicolor/*/apps/%{name}.*
%{_mandir}/man1/%{name}*.1.*
