# CyberDollar Core 1.7 Alpha
=========================

CyberDollar Core 1.7 is a complete re-architecture of CyberDollar, changing from
using the Litecoin client as its base, to Bitcoin 0.9. It's still CyberDollar,
with the same Scrypt PoW algorithm, same reward schedule, but there are a 
lot of changes under the hood.


For the full Bitcoin 0.9 changelog, please see https://bitcointalk.org/index.php?topic=522014

Please note that this is a very early release, and a full audit of the code
is still in progress. The client has been hard-coded to only work with testnet
for now, to avoid the risk of damaging real wallets.


Downgrading
-----------

First and foremost, please note that downgrading from 1.7 to 1.6 is not trivial.
1.7 now uses Berkeley DB 5.1 as its default database (in place of 4.8), and as
such may create database files which are incompatible with previous versions.

Rebranding to CyberDollar Core
---------------------------

Following in the footsteps of Bitcoin (Core), the CyberDollar reference client
has been rebranded as "CyberDollar Core". This helps separate its identity
from CyberDollar (the network).

cyberdollar-cli
------------

Where previously commands were sent to cyberdollard by running
"cyberdollard <command>", 1.7 adopts the model from Bitcoin Core 0.9 where there is
a separate "cyberdollar-cli" executable which is used instead. This avoids the risk
of accidentally trying to start two daemons at the same time, for example.


Transaction malleability-related fixes
--------------------------------------

Fixes for risk-cases involving transaction malleability have been added; this
is particularly important for any merchants or exchanges using the built-in
wallet system. 

Testnet
-------

As mentioned at the start of this document, the alpha-client is for use with the
CyberDollar testnet only. This is an alternative CyberDollar blockchain which is
not used for real transactions, and instead is intended for testing of experimental
clients. Wallets and addresses are incompatible with the normal CyberDollar
network, in order to isolate the two.

As "TestCyber" is essentially valueless, it can be acquired easily for testing,
either by mining, or from a faucet such as http://testcyber.lionservers.de/
