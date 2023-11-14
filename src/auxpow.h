// Copyright (c) 2009-2010 Satoshi Nakamoto
// Copyright (c) 2009-2014 The Australiacash developers
// Copyright (c) 2014-2016 Daniel Kraft
// Distributed under the MIT/X11 software license, see the accompanying
// file license.txt or http://www.opensource.org/licenses/mit-license.php.

#ifndef BITCOIN_AUXPOW_H
#define BITCOIN_AUXPOW_H

#include <consensus/params.h>
#include <primitives/pureheader.h>
#include <primitives/transaction.h>
#include <serialize.h>
#include <uint256.h>

#include <memory>
#include <vector>

class CBlock;
class CBlockHeader;
class CBlockIndex;
class CValidationState;
class UniValue;

namespace auxpow_tests
{
class CAuxPowForTest;
}

static const unsigned char pchMergedMiningHeader[] = {0xfa, 0xbe, 'm', 'm'};

class CBaseMerkleTx
{
public:
    CTransactionRef tx;
    uint256 hashBlock;
    std::vector<uint256> vMerkleBranch;
    int nIndex;

    CBaseMerkleTx()
    {
        SetTx(MakeTransactionRef());
        Init();
    }

    explicit CBaseMerkleTx(CTransactionRef arg)
    {
        SetTx(std::move(arg));
        Init();
    }

    CBaseMerkleTx(CTransactionRef arg, int index)
    {
        SetTx(std::move(arg));
        Init();
        nIndex = index;
    }

    void Init()
    {
        hashBlock = uint256();
        nIndex = -1;
    }

    void SetTx(CTransactionRef arg)
    {
        tx = std::move(arg);
    }

    ADD_SERIALIZE_METHODS;

    template <typename Stream, typename Operation>
    inline void SerializationOp(Stream &s, Operation ser_action)
    {
        READWRITE(tx);
        READWRITE(hashBlock);
        READWRITE(vMerkleBranch);
        READWRITE(nIndex);
    }

    const uint256 &GetHash() const { return tx->GetHash(); }
};

class CAuxPow
{

private:
    CBaseMerkleTx coinbaseTx;
    std::vector<uint256> vChainMerkleBranch;
    int nChainIndex;
    CPureBlockHeader parentBlock;

    static uint256 CheckMerkleBranch(uint256 hash,
                                      const std::vector<uint256> &vMerkleBranch,
                                      int nIndex);

    friend UniValue AuxpowToJSON(const CAuxPow &auxpow);
    friend class auxpow_tests::CAuxPowForTest;

public:
    inline explicit CAuxPow(CTransactionRef txIn)
        : coinbaseTx(txIn) {}

    CAuxPow() = default;

    ADD_SERIALIZE_METHODS;

    template <typename Stream, typename Operation>
    inline void SerializationOp(Stream &s, Operation ser_action)
    {
        READWRITE(coinbaseTx);
        READWRITE(vChainMerkleBranch);
        READWRITE(nChainIndex);
        READWRITE(parentBlock);
    }

    bool check(const uint256 &hashAuxBlock, int nChainId,
               const Consensus::Params &params) const;

    inline uint256 getParentBlockPoWHash() const
    {
        return parentBlock.GetPoWHash();
    }

    inline const CPureBlockHeader &getParentBlock() const
    {
        return parentBlock;
    }

    static int getExpectedIndex(uint32_t nNonce, int nChainId, unsigned h);

    static std::unique_ptr<CAuxPow> createAuxPow(const CPureBlockHeader &header);

    static CPureBlockHeader &initAuxPow(CBlockHeader &header);
};

#endif // BITCOIN_AUXPOW_H

