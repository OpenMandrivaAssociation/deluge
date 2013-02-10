# Use system or static libtorrent(-rasterbar)?
%define sys_libtorrent	1
%define _enable_debug_packages %nil
%define debug_package %nil

Summary:	Full-featured GTK+ Bittorrent client
Name:		deluge
Version:	1.3.5
Release:	2
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


%changelog
* Wed Apr 11 2012 Andrey Bondrov <abondrov@mandriva.org> 1.3.5-1
+ Revision: 790275
- New version 1.3.5

* Tue Mar 06 2012 Andrey Bondrov <abondrov@mandriva.org> 1.3.4-1
+ Revision: 782358
- Don't use find_lang because it finds nothing
- New version 1.3.4

* Thu Aug 18 2011 Tomasz Pawel Gajc <tpg@mandriva.org> 1.3.3-1
+ Revision: 695247
- add buildrequires on intltool
- temporary disable build of debug package
- skip another build at installa section
- dont use desktop-file-install
- update to new version 1.3.3

* Wed May 25 2011 Funda Wang <fwang@mandriva.org> 1.3.2-1
+ Revision: 678936
- update file list
- new version 1.3.2

* Tue Nov 02 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.3.1-1mdv2011.0
+ Revision: 591840
- update to 1.3.1

* Sun Sep 19 2010 Funda Wang <fwang@mandriva.org> 1.3.0-1mdv2011.0
+ Revision: 579768
- 1.3.0 final

* Wed Aug 25 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.3.0-0.rc2.1mdv2011.0
+ Revision: 573340
- update to 1.3.0_rc2

* Sun Aug 01 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.3.0-0.rc1.1mdv2011.0
+ Revision: 564168
- change spec to make it more easier to package rc's (since quite a few rc's go
  into cooker), (thanks to the meticulous transmission.spec)
- remove 'mdkversion < 200900' bits, too old
- add a patch from Debian to disable checking for updates in the gui (replaces
  patch0 which doesn't seem to work now)
- update to 1.3.0_rc1
- drop patch2, merged upstream

* Sat May 15 2010 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.3-2mdv2010.1
+ Revision: 544853
- Patch2: fix hangs on shutdown when using sys tray menu

* Sun Mar 28 2010 Eugeni Dodonov <eugeni@mandriva.com> 1.2.3-1mdv2010.1
+ Revision: 528344
- Updated to 1.2.3.

* Sat Mar 20 2010 Emmanuel Andry <eandry@mandriva.org> 1.2.2-1mdv2010.1
+ Revision: 525432
- New version 1.2.2

* Tue Feb 23 2010 Ahmad Samir <ahmadsamir@mandriva.org> 1.2.1-2mdv2010.1
+ Revision: 509933
- 1.2.1 requires libtorrent-rasterbar >= 0.14.9 to fix an over-downloading bug
  in older versions of libtorrent-rasterbar (c.f. 1.2.1 changelog in the src tarball)

* Mon Feb 22 2010 Frederik Himpe <fhimpe@mandriva.org> 1.2.1-1mdv2010.1
+ Revision: 509638
- update to new version 1.2.1

* Tue Jan 12 2010 Jérôme Brenier <incubusss@mandriva.org> 1.2.0-1mdv2010.1
+ Revision: 490022
- final release 1.2.0
- use lzma source tarball

* Fri Dec 18 2009 Ahmad Samir <ahmadsamir@mandriva.org> 1.2.0-0.rc5.1mdv2010.1
+ Revision: 479923
- update to 1.2.0_rc5

* Fri Nov 27 2009 Ahmad Samir <ahmadsamir@mandriva.org> 1.2.0-0.rc4.1mdv2010.1
+ Revision: 470632
- Update to new version 1.2.0_rc4

* Thu Nov 19 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.2.0-0.rc3.1mdv2010.1
+ Revision: 467513
- update to new version 1.2.0_rc3
- add requires on python-chardet, python-OpenSSL, python-notify, python-simplejson and python-twisted-web
- drop requires on python-dbus

* Tue Jun 16 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.9-1mdv2010.0
+ Revision: 386425
- update to new version 1.1.9

* Fri May 22 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.1.8-1mdv2010.0
+ Revision: 378581
- Updated to 1.1.8.
  Rediffed P1.

* Fri May 01 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.1.7-1mdv2010.0
+ Revision: 369210
- 1.1.7

* Sat Apr 18 2009 Eugeni Dodonov <eugeni@mandriva.com> 1.1.6-1mdv2009.1
+ Revision: 367974
- Updated to 1.1.6.

* Wed Mar 18 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.5-1mdv2009.1
+ Revision: 357019
- Update to new version 1.1.5

* Wed Mar 11 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.4-1mdv2009.1
+ Revision: 353924
- update to new version 1.1.4

* Mon Feb 16 2009 Frederik Himpe <fhimpe@mandriva.org> 1.1.3-1mdv2009.1
+ Revision: 341109
- update to new version 1.1.3

* Wed Feb 04 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.2-1mdv2009.1
+ Revision: 337473
- update to new version 1.1.2

* Sun Jan 25 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.1-1mdv2009.1
+ Revision: 333564
- update to new version 1.1.1

* Tue Jan 13 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.0-1mdv2009.1
+ Revision: 329058
- update to new version 1.1.0

* Sat Jan 10 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.0-0.RC3.1mdv2009.1
+ Revision: 328133
- update to new version 1.1.0_RC3

* Mon Jan 05 2009 Tomasz Pawel Gajc <tpg@mandriva.org> 1.1.0-0.RC2.1mdv2009.1
+ Revision: 325154
- drop patch 2, fixed upstream
- update to new version 1.1.0_RC2

* Wed Dec 24 2008 Michael Scherer <misc@mandriva.org> 1.0.7-4mdv2009.1
+ Revision: 318428
- rebuild for new python

* Sun Dec 21 2008 Funda Wang <fwang@mandriva.org> 1.0.7-3mdv2009.1
+ Revision: 316919
- rebuild for new boost

* Tue Dec 16 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.7-2mdv2009.1
+ Revision: 314920
- make file list conditional on system libtorrent build
- drop the python version check (all now supported releases are 2.5+)
- adjust file list for noarch
- doesn't actually br the libtorrent devel package, it only needs python module
- use system libtorrent-rasterbar by default (yaay) - package now noarch
- add a newer (and smaller) set of conditionals for building with system
  libtorrent-rasterbar
- drop the old system libtorrent commented stuff, it's all outdated now

* Sun Dec 14 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.7-1mdv2009.1
+ Revision: 314369
- update to new version 1.0.7
- Patch1: rediff

  + Oden Eriksson <oeriksson@mandriva.com>
    - lowercase ImageMagick

* Tue Dec 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.6-1mdv2009.1
+ Revision: 309498
- fix file list
- update to new version 1.0.6

* Tue Dec 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.5-3mdv2009.1
+ Revision: 309495
- rebuild

* Sat Nov 29 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.5-2mdv2009.1
+ Revision: 308008
- require python-pkg-resources for mdv version greater than 200900, instead of python-setuptools which requires bunch of useless python stuff and python-devel

* Tue Nov 11 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.5-1mdv2009.1
+ Revision: 302126
- update to new version 1.0.5

* Sun Nov 02 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.4-1mdv2009.1
+ Revision: 299306
- update to new version 1.0.4

* Tue Oct 21 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 1.0.3-1mdv2009.1
+ Revision: 296203
- update to new version 1.0.3

* Sun Oct 12 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.2-1mdv2009.1
+ Revision: 292606
- rediff use-multithreaded-boost.patch
- new version 1.0.2

* Wed Sep 24 2008 Adam Williamson <awilliamson@mandriva.org> 1.0.0-1mdv2009.0
+ Revision: 287867
- fix setup macro
- improve use-multithreaded-boost.patch to reliably do what we want with
  upstream's braindead boost detection on i586 and x86-64
- don't use %%{name} in patch names
- correct license (now GPLv3+, and has an openssl exception)
- adjust summary and description: users don't care what language it's in
- new release 1.0.0

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - update to new version 0.9.09

* Thu Aug 28 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.08-2mdv2009.0
+ Revision: 276742
- update to new release candidate 0.9.08
- fix url for source

* Mon Aug 18 2008 Tomasz Pawel Gajc <tpg@mandriva.org> 0.9.07-1mdv2009.0
+ Revision: 273468
- update to new version 0.9.07
- Patch1: use multithreaded boost libraries
- improve summary
- spec file clean

  + Per Øyvind Karlsen <peroyvind@mandriva.org>
    - rebuild against new boost

* Thu Aug 14 2008 Funda Wang <fwang@mandriva.org> 0.9.06-1mdv2009.0
+ Revision: 272033
- New version 0.9.06

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - add build requires and runtime requires on python-setuptools

* Thu Aug 07 2008 Funda Wang <fwang@mandriva.org> 0.9.05-1mdv2009.0
+ Revision: 265693
- New version 0.9.05
- rediff update patch

* Thu Jun 26 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.9.3-1mdv2009.0
+ Revision: 229190
- new release 0.5.9.3

* Sun Jun 22 2008 Funda Wang <fwang@mandriva.org> 0.5.9.2-1mdv2009.0
+ Revision: 227874
- New version 0.5.9.2

  + Pixel <pixel@mandriva.com>
    - rpm filetriggers deprecates update_menus/update_scrollkeeper/update_mime_database/update_icon_cache/update_desktop_database/post_install_gconf_schemas

  + Adam Williamson <awilliamson@mandriva.org>
    - add update.patch to disable update notification by default
    - new release 0.5.9.1

* Thu May 01 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.9.0-1mdv2009.0
+ Revision: 199845
- drop versioncheck.patch: upstream default was changed to off
- new release 0.5.9.0

* Thu Apr 17 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.8.9-1mdv2009.0
+ Revision: 195190
- new release 0.5.8.9

* Sat Apr 12 2008 trem <trem@mandriva.org> 0.5.8.7-1mdv2009.0
+ Revision: 192617
- update to 0.5.8.7

* Thu Mar 20 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.8.6-1mdv2008.1
+ Revision: 189224
- new release 0.5.8.6 (bugfixes)

* Sun Mar 02 2008 trem <trem@mandriva.org> 0.5.8.5-1mdv2008.1
+ Revision: 177790
- update to 0.5.8.5

* Sat Feb 23 2008 Adam Williamson <awilliamson@mandriva.org> 0.5.8.4-1mdv2008.1
+ Revision: 174059
- rediff versioncheck.patch, and don't bother patching the Windows default options any more in it
- new release 0.5.8.4

* Sat Feb 02 2008 Funda Wang <fwang@mandriva.org> 0.5.8.3-1mdv2008.1
+ Revision: 161327
- New version 0.5.8.3

* Sun Jan 27 2008 Funda Wang <fwang@mandriva.org> 0.5.8.2-1mdv2008.1
+ Revision: 158539
- New version 0.5.8.2

  + Adam Williamson <awilliamson@mandriva.org>
    - new release 0.5.8.1

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

* Sun Dec 30 2007 Funda Wang <fwang@mandriva.org> 0.5.8-1mdv2008.1
+ Revision: 139517
- New version 0.5.8

* Thu Dec 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.7.98-1mdv2008.1
+ Revision: 138666
- rediff versioncheck.patch
- re-add French translation to see if it works yet (cf. http://forum.mandriva.com/viewtopic.php?t=77442)
- new version 0.5.7.98 (0.5.8 RC2)

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request

* Mon Dec 03 2007 Funda Wang <fwang@mandriva.org> 0.5.7.1-1mdv2008.1
+ Revision: 114529
- New version 0.5.7.1
- fix requires on librsvg

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - correct requires on librsvg2

* Tue Nov 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.6.96-1mdv2008.1
+ Revision: 113520
- new release 0.5.6.96

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - add missing requires

* Fri Nov 02 2007 Götz Waschk <waschk@mandriva.org> 0.5.6.2-2mdv2008.1
+ Revision: 105179
- drop patch 0 and build with new boost

* Thu Nov 01 2007 Funda Wang <fwang@mandriva.org> 0.5.6.2-1mdv2008.1
+ Revision: 104332
- New version 0.5.6.1
- rediff boost patch

* Tue Oct 30 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.6.1-1mdv2008.1
+ Revision: 103898
- rediff boost patch
- new release 0.5.6.1

* Thu Oct 25 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.6-1mdv2008.1
+ Revision: 102022
- adjust icon stuff for upstream changes
- rediff boost patch
- new release 0.5.6
- new release 0.5.6

* Sun Oct 21 2007 Olivier Blin <blino@mandriva.org> 0.5.5-3mdv2008.1
+ Revision: 101030
- require gnome-python-gnomevfs
- require pygtk2.0-libglade

* Sun Oct 21 2007 Götz Waschk <waschk@mandriva.org> 0.5.5-2mdv2008.1
+ Revision: 100910
- fix build with new boost

* Wed Oct 10 2007 Funda Wang <fwang@mandriva.org> 0.5.5-1mdv2008.1
+ Revision: 96832
- New version 0.5.5

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - fix icons installation

* Thu Sep 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.4.1-3mdv2008.0
+ Revision: 93341
- update icon name fix (png vs. xpm)
- remove the French translation, it's broken somehow and I don't know how to fix
- re-adopt some of tpg's cleanups
- correct license
- add deluge-0.5.4.1-versioncheck.patch to disable the new version check
- revert to 0.5.4.1 per maintainers@ post

  + Tomasz Pawel Gajc <tpg@mandriva.org>
    - spec file clean
    - handle nicely installation of icons
    - do not hardcode icon extension in desktop file
    - new version

* Sun Aug 12 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.4.1-1mdv2008.0
+ Revision: 62298
- new release 0.5.4.1

* Thu Aug 09 2007 Funda Wang <fwang@mandriva.org> 0.5.4-1mdv2008.0
+ Revision: 60901
- New version 0.5.4
- rediff patch

* Fri Jul 27 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.3-1mdv2008.0
+ Revision: 56130
- new release 0.5.3

* Sat Jul 21 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.2.90-1mdv2008.0
+ Revision: 54331
- test for python version not MDV version in determining whether to include certain python files (this is more correct)
- revise size range and generation strategy for fd.o icons
- drop old icons
- specify license as GPLv2
- clean spec (tabs, consistent variables)
- new release 0.5.2.90 (0.5.3 RC1)
- bump to retry backport

* Fri Jul 06 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.2-1mdv2008.0
+ Revision: 49233
- rediff patch0
- new release 0.5.2

* Sun Jul 01 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.1.90-1mdv2008.0
+ Revision: 46191
- new release 0.5.1.90 (0.5.2 RC1); rediff patch0

* Sat Jun 16 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.1.1-1mdv2008.0
+ Revision: 40349
- okay, try fixing the boost issue another way
- fix distro test in setup.py for releases other than 2007.1
- new release 0.5.1.1, some spec cleaning
- real fix for 2007.0 build (the file apparently doesn't exist under python 2.4 at all)

* Fri Apr 20 2007 Adam Williamson <awilliamson@mandriva.org> 0.5.0-3mdv
+ Revision: 16367
- fix build on 2007.0 (remove specific reference to python 2.5 file in files list)


* Wed Mar 21 2007 Adam Williamson <awilliamson@mandriva.com> 0.5.0-2mdv2007.1
+ Revision: 147655
- generate fd.o icons in spec, use them in .desktop

* Mon Mar 19 2007 Adam Williamson <awilliamson@mandriva.com> 0.5.0-1mdv2007.1
+ Revision: 146380
- drop the patch (fixed upstream)
- 0.5.0 final
- Import deluge

  + Michael Scherer <misc@mandriva.org>
    - fix french translation

