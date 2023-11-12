// Copyright (c) 2020 The AustraliaCash Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef BITCOIN_RPC_MINING_H
#define BITCOIN_RPC_MINING_H

/** Default max timeout whilst mining in RPC generatetodescriptor, generatetoaddress, and generateblock. */
static const uint64_t DEFAULT_MAX_TIMEOUT{60};

/** Singleton instance of the AuxpowMiner, created during startup.  */
extern std::unique_ptr<AuxpowMiner> g_auxpow_miner;

#endif // BITCOIN_RPC_MINING_H
