// Copyright (c) 2021 The AustraliaCash developers
// Distributed under the MIT/X11 software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#ifndef AUSTRALIACASH_AUXPOW_FORK_PARAMS_H
#define AUSTRALIACASH_AUXPOW_FORK_PARAMS_H

const int AUXPOW_CHAIN_ID = 0x205e;         // To be consistent with previous block version 0x20000000
const int AUXPOW_START_HEIGHT = 800000;    // Right before the halving?
const int LWMA_START_HEIGHT = 900000;   // After halving, also starts 30 sec blocktime.
#endif // AUSTRALIACASH_AUXPOW_FORK_PARAMS_H
