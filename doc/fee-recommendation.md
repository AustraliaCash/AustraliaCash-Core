CyberDollar Fee Recommendation
----------------------------

_last updated for 1.14.6_

The CyberDollar chain has a relatively low block interval, 1 megabyte blockspace
and aims to provide a cheap means for people to transact. Therefore, the biggest
threat to the CyberDollar chain as a whole is spam and in 2014, a transaction fee
and dust disincentive were introduced, to combat on-chain spam.

CyberDollar Core implements a number of defaults into the software that reflect the
developers' recommendations towards fees and dust limits, that at the moment of
release represent the developers best estimate of how these limits should be
parametrized. The recommended defaults, as implemented in the CyberDollar Core
wallet, are:

- **0.01 CASH per kilobyte** transaction fee
- **0.01 CASH** dust limit (discard threshold)
- **0.001 CASH** replace-by-fee increments

The wallet rejects transactions that have outputs under the dust limit, and
discards change to fee if it falls under this limit.

Note: In the past, CyberDollar has enforced a rounding function in the fee
      mechanism. Since version 1.14.5, this is no longer the case, and fees are
      calculated over the exact size of a transaction. For example, a 192 byte
      transaction only has to pay `0.01 / 1000 * 192 = 0.00192` CASH fee.

## Miner default inclusion policies

The default values for miners to include a transaction in a block has been set
to exactly the recommended fee of **0.01 CASH/kB.** Dust limits are defined by
the miner's mempool policy, see below.

## Relay and mempool policies

The relay and mempool acceptance policies are lower than the recommendations
by default, to allow for a margin to change recommendations in the future (or
user preference) without the need for an adopted software release in advance.
This greatly simplifies future policy recommendations. As historically, most
relay nodes do not change these default settings, these often represent an
absolute mininum

### Transaction fee

The default minimum transaction fee for relay is set at **0.001 CASH/kB**,
exactly one-tenth of the recommended fee. This gives miners and relay operators
a 10x downward margin to operate within from a spam management perspective.

### Dust limits

The mempool logic implements 2 dust limits, a hard dust limit under which a
transactions is considered non-standard and rejected, and a soft dust limit
that requires the limit itself to be added to the transaction fee, making the
output economically unviable.

- The hard dust limit is set at **0.001 CASH** - outputs under this value are
  invalid and rejected.
- The soft dust limit is set at **0.01 CASH** - sending a transaction with outputs
  under this value, are required to add 0.01 CASH for each such output, or else
  will be considered to have too low fee and be rejected.

### Replace-by-fee and mempool limiting increments

The increments used for replace-by-fee and limiting the mempool once it has
reached its locally defined maximum size, is by default set at one-tenth of
the relay fee, or **0.0001 CASH**.
