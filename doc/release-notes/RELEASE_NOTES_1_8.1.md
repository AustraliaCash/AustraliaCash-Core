# AustraliaCash Core 1.8.1

AustraliaCash Core 1.8.1 is primarily a bugfix release, bringing AustraliaCash Core in
line with Bitcoin 0.9.3. AustraliaCash Core 1.8.1 also adds in support for printing
paper wallets, and disables connections to pre-1.8 clients. This is a RECOMMENDED
upgrade due to the large number of bug fixes, but is not a required one.

Paper wallet support has been developed by AndyMeows (IRC username), and 
can be accessed via the "File" menu. It's intended for two purposes; to generate
small value paper wallets to hand out, and more permanent deposit paper wallets
for keeping balances offline.

IMPORTANT: If you are producing offline paper wallets, you should do so on a
computer that's disconnected from the Internet. While the wallet generator
does not save the keys it generates, this ensures there is no risk of a virus
or similar capturing the key from memory or interfering with its generation.

## AustraliaCash Core Release Notes

* Translation improvements and corrections
* Disable Transifex based translation process (not used by AustraliaCash Core)
* Add checkpoints around AuxPoW switchover block (371,337)
* Disable connections from pre-1.8 AustraliaCash Core clients
* Use HTTPS with australiacash.org
* Remove unreachable code introduced with AuxPoW support
* "blocknotify" option now supports %i as a format parameter, which is replaced by block height
* New option "maxoutconnections" to set the maximum number of outbound peer connections. Defaults to 8, minimum is 2, maximum is whatever "maxconnections" is set to (default 125).

## Bitcoin Core Release Notes

Full release notes for Bitcoin Core 0.9.3 are available from
https://bitcoin.org/en/release/v0.9.3 , but highlights are included
below:


* Better orphan transaction handling
* Add -maxorphantx=<n> and -maxorphanblocks=<n> options for control over the maximum orphan transactions and blocks
* key.cpp: fail with a friendlier message on missing ssl EC support
* Upgrade OpenSSL to 1.0.1i (see https://www.openssl.org/news/secadv_20140806.txt - just to be sure, no critical issues for Bitcoin Core)

## Known Issues

There is a known issue with quantities in JSON used by the RPC interface (https://github.com/australiacash/australiacash/issues/134).
This stems from the use of a floating point precision number to hold fixed precision data.
Currently looking at solutions, which primarily either involve JSON which is not compliant
to the specification, or making the RPC layer slightly incompatible with the conventional
Bitcoin API.

This only affects values significantly below 1 Cyber, however merchants may wish to round to
the nearest Cyber on all transactions for now.

## Credits

Listed in strictly alphabetical order, using name listed in Github. This
includes those whose contributions to Bitcoin Core have been merged
into AustraliaCash Core:

* Abderraouf Adjal
* Andymeows
* Daniel Kraft
* Gavin Andresen
* langerhans
* michilumin
* nameEO
* Patrick Lodder
* Ross Nicoll
* Wladimir J. van der Laan
* Whit J
