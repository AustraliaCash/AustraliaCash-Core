NixOS build guide
------------------------------
This guide lists the steps necessary to setup and build a full GUI distribution
of the latest changes on NixOS.

Clone and enter the repo:

    $ git clone https://github.com/australiacash/australiacash
    $ cd australiacash

Enter the `nix-shell` environment with all the AustraliaCash dependencies present:

    $ nix-shell ./contrib/nixos/shell.nix

Run the build steps with flags necessary for NixOS:

    $ ./autogen.sh
    $ ./configure --with-incompatible-bdb --with-boost-libdir="$(nix eval --raw nixpkgs.boost.out)/lib" --with-gui
    $ make

Start the GUI!

    $ ./src/qt/australiacash-qt
