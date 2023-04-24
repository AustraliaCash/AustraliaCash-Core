
Debian
====================
This directory contains files used to package cyberdollard/cyberdollar-qt
for Debian-based Linux systems. If you compile cyberdollard/cyberdollar-qt yourself, there are some useful files here.

## cyberdollar: URI support ##


cyberdollar-qt.desktop  (Gnome / Open Desktop)
To install:

	sudo desktop-file-install cyberdollar-qt.desktop
	sudo update-desktop-database

If you build yourself, you will either need to modify the paths in
the .desktop file or copy or symlink your cyberdollar-qt binary to `/usr/bin`
and the `../../share/pixmaps/cyberdollar128.png` to `/usr/share/pixmaps`

cyberdollar-qt.protocol (KDE)

