// Copyright (c) 2015-2021 The CyberDollar Core developers
// Distributed under the MIT software license, see the accompanying
// file COPYING or http://www.opensource.org/licenses/mit-license.php.

#include <boost/random/uniform_int.hpp>
#include <boost/random/mersenne_twister.hpp>

#include "policy/policy.h"
#include "arith_uint256.h"
#include "cyberdollar.h"
#include "txmempool.h"
#include "util.h"
#include "validation.h"
#include "cyberdollar-fees.h"

int static generateMTRandom(unsigned int s, int range)
{
    boost::mt19937 gen(s);
    boost::uniform_int<> dist(1, range);
    return dist(gen);
}

bool AllowDigishieldMinDifficultyForBlock(const CBlockIndex* pindexLast, const CBlockHeader *pblock, const Consensus::Params& params)
{
    if (!params.fPowAllowMinDifficultyBlocks)
        return false;

    if (!params.fPowAllowDigishieldMinDifficultyBlocks)
        return false;

    return (pblock->GetBlockTime() > pindexLast->GetBlockTime() + params.nPowTargetSpacing * 8);
}

unsigned int CalculateCyberdollarNextWorkRequired(const CBlockIndex* pindexLast, int64_t nFirstBlockTime, const Consensus::Params& params)
{
    int nHeight = pindexLast->nHeight + 1;
    int64_t retargetTimespan = params.nPowTargetTimespan;
    int64_t nActualTimespan = pindexLast->GetBlockTime() - nFirstBlockTime;
    int64_t nModulatedTimespan = nActualTimespan;
    int64_t nMaxTimespan;
    int64_t nMinTimespan;

    // Pre-block 815,000
    if (nHeight < 815000) {
        if (params.fDigishieldDifficultyCalculation) {
            nModulatedTimespan = retargetTimespan + (nModulatedTimespan - retargetTimespan) / 8;
            nMinTimespan = retargetTimespan - (retargetTimespan / 4);
            nMaxTimespan = retargetTimespan + (retargetTimespan / 2);
        } else if (nHeight > 10000) {
            nMinTimespan = retargetTimespan / 4;
            nMaxTimespan = retargetTimespan * 4;
        } else if (nHeight > 5000) {
            nMinTimespan = retargetTimespan / 8;
            nMaxTimespan = retargetTimespan * 4;
        } else {
            nMinTimespan = retargetTimespan / 16;
            nMaxTimespan = retargetTimespan * 4;
        }
    }
    // Post-block 1,000,000 - Adaptive adjustments
    else {
        // Shorter timespan and smoother adjustment
        retargetTimespan = params.nPowTargetTimespan / 2;
        nModulatedTimespan = retargetTimespan + (nModulatedTimespan - retargetTimespan) / 4;

        // Limit difficulty changes to avoid spikes
        nMinTimespan = retargetTimespan / 2;  // Halve the minimum timespan allowed
        nMaxTimespan = retargetTimespan * 2;  // Double the maximum timespan allowed

        // Introduce a difficulty averaging filter
        int64_t nBlockTimeAvg = 0;
        int nLookbackWindow = 10;
        const CBlockIndex* pindexWalk = pindexLast;
        for (int i = 0; i < nLookbackWindow && pindexWalk != nullptr; ++i) {
            nBlockTimeAvg += pindexWalk->GetBlockTime();
            pindexWalk = pindexWalk->pprev;
        }
        nBlockTimeAvg /= nLookbackWindow;

        // If average block time exceeds 4x the target spacing, use minimum difficulty
        if (nBlockTimeAvg > pindexLast->GetBlockTime() + params.nPowTargetSpacing * 4) {
            return params.powLimit.GetCompact();
        }
    }

    // Apply limits to difficulty adjustments
    if (nModulatedTimespan < nMinTimespan)
        nModulatedTimespan = nMinTimespan;
    else if (nModulatedTimespan > nMaxTimespan)
        nModulatedTimespan = nMaxTimespan;

    // Retarget
    const arith_uint256 bnPowLimit = UintToArith256(params.powLimit);
    arith_uint256 bnNew;
    arith_uint256 bnOld;
    bnNew.SetCompact(pindexLast->nBits);
    bnOld = bnNew;
    bnNew *= nModulatedTimespan;
    bnNew /= retargetTimespan;

    // Ensure difficulty doesn't exceed the pow limit
    if (bnNew > bnPowLimit)
        bnNew = bnPowLimit;

    return bnNew.GetCompact();
}

bool CheckAuxPowProofOfWork(const CBlockHeader& block, const Consensus::Params& params)
{
    if (!block.IsLegacy() && params.fStrictChainId && block.GetChainId() != params.nAuxpowChainId)
        return error("%s : block does not have our chain ID"
                     " (got %d, expected %d, full nVersion %d)",
                     __func__, block.GetChainId(),
                     params.nAuxpowChainId, block.nVersion);

    if (!block.auxpow) {
        if (block.IsAuxpow())
            return error("%s : no auxpow on block with auxpow version", __func__);

        if (!CheckProofOfWork(block.GetPoWHash(), block.nBits, params))
            return error("%s : non-AUX proof of work failed", __func__);

        return true;
    }

    if (!block.IsAuxpow())
        return error("%s : auxpow on block with non-auxpow version", __func__);

    if (!block.auxpow->check(block.GetHash(), block.GetChainId(), params))
        return error("%s : AUX POW is not valid", __func__);
    if (!CheckProofOfWork(block.auxpow->getParentBlockPoWHash(), block.nBits, params))
        return error("%s : AUX proof of work failed", __func__);

    return true;
}

CAmount GetCyberDollarBlockSubsidy(int nHeight, const Consensus::Params& consensusParams, uint256 prevHash)
{
    int halvings = nHeight / consensusParams.nSubsidyHalvingInterval;

    if (!consensusParams.fSimplifiedRewards)
    {
        // Current-style rewards derived from the previous block hash
        const std::string cseed_str = prevHash.ToString().substr(7, 7);
        const char* cseed = cseed_str.c_str();
        char* endp = NULL;
        long seed = strtol(cseed, &endp, 16);
        CAmount maxReward = (1000000 >> halvings) - 1;
        int rand = generateMTRandom(seed, maxReward);

        return (1 + rand) * COIN;
    } else if (nHeight < (13 * consensusParams.nSubsidyHalvingInterval)) {
        // New-style constant rewards for each halving interval - Not Active
        return (500000 * COIN) >> halvings;
    } else {
        // Constant inflation
        return 100 * COIN;
    }
}


