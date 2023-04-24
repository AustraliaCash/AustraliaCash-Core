#!/usr/bin/env python3
# Copyright (c) 2014-2016 The Bitcoin Core developers
# Copyright (c) 2021 The CyberDollar Core developers
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

#
# Test pruning code
# ********
# WARNING:
# This test uses 21GB of disk space.
# This test takes 20 mins or more (up to 2 hours)
# ********
from test_framework.blocktools import create_coinbase
from test_framework.mininode import CBlock
from test_framework.script import (
    CScript,
    OP_NOP,
    OP_RETURN,
)
from test_framework.test_framework import BitcoinTestFramework
from test_framework.util import (
    start_node,
    connect_nodes,
    sync_blocks,
    assert_equal,
    assert_greater_than,
    assert_raises_jsonrpc,
)
import time
import os

# Rescans start at the earliest block up to 2 hours before a key timestamp, so
# the manual prune RPC avoids pruning blocks in the same window to be
# compatible with pruning based on key creation time.
RESCAN_WINDOW = 2 * 60 * 60

def mine_large_blocks(node, n):
    # Make a large scriptPubKey for the coinbase transaction. This is OP_RETURN
    # followed by 950k of OP_NOP. This would be non-standard in a non-coinbase
    # transaction but is consensus valid.

    # Set the nTime if this is the first time this function has been called.
    # A static variable ensures that time is monotonicly increasing and is therefore
    # different for each block created => blockhash is unique.
    if "nTimes" not in mine_large_blocks.__dict__:
        mine_large_blocks.nTime = 0
        
    # Get the block parameters for the first block
    big_script = CScript([OP_RETURN] + [OP_NOP] * 950000)
    best_block = node.getblock(node.getbestblockhash())
    height = int(best_block["height"]) + 1
    mine_large_blocks.nTime = max(mine_large_blocks.nTime, int(best_block["time"])) + 1
    previousblockhash = int(best_block["hash"], 16)

    for _ in range(n):
        # Build the coinbase transaction (with large scriptPubKey)
        coinbase_tx = create_coinbase(height)
        coinbase_tx.vin[0].nSequence = 2 ** 32 - 1
        coinbase_tx.vout[0].scriptPubKey = big_script
        coinbase_tx.rehash()

        # Build the block
        block = CBlock()
        block.nVersion = 0x620004
        block.hashPrevBlock = previousblockhash
        block.nTime = mine_large_blocks.nTime
        block.nBits = int('207fffff', 16)
        block.nNonce = 0
        block.vtx = [coinbase_tx]
        block.hashMerkleRoot = block.calc_merkle_root()
        block.calc_sha256()
        block.solve()

        # Submit to the node
        node.submitblock(block.serialize().hex())

        previousblockhash = block.sha256
        height += 1
        mine_large_blocks.nTime += 1

def calc_usage(blockdir):
    return sum(os.path.getsize(blockdir+f) for f in os.listdir(blockdir) if os.path.isfile(blockdir+f)) / (1024. * 1024.)

class PruneTest(BitcoinTestFramework):

    def __init__(self):
        super().__init__()
        self.setup_clean_chain = True
        self.num_nodes = 6

    def setup_network(self):
        self.nodes = []
        self.is_network_split = False

        # Create nodes 0 and 1 to mine
        self.nodes.append(start_node(0, self.options.tmpdir, ["-debug", "-maxreceivebuffer=20000"], timewait=1200))
        self.nodes.append(start_node(1, self.options.tmpdir, ["-debug", "-maxreceivebuffer=20000"], timewait=1200))

        # Create node 2 to test pruning
        self.nodes.append(start_node(2, self.options.tmpdir, ["-debug", "-maxreceivebuffer=20000", "-prune=2200"], timewait=1200))
        self.prunedir = self.options.tmpdir+"/node2/regtest/blocks/"

        # Create nodes 3 and 4 to test manual pruning (they will be re-started with manual pruning later)
        self.nodes.append(start_node(3, self.options.tmpdir, ["-debug=0", "-maxreceivebuffer=20000"], timewait=1200))
        self.nodes.append(start_node(4, self.options.tmpdir, ["-debug=0", "-maxreceivebuffer=20000"], timewait=1200))

        # Create nodes 5 to test wallet in prune mode, but do not connect
        self.nodes.append(start_node(5, self.options.tmpdir, ["-debug=0", "-prune=2200"]))

        # Determine default relay fee
        self.relayfee = self.nodes[0].getnetworkinfo()["relayfee"]

        connect_nodes(self.nodes[0], 1)
        connect_nodes(self.nodes[1], 2)
        connect_nodes(self.nodes[2], 0)
        connect_nodes(self.nodes[3], 4)
        sync_blocks(self.nodes[0:5])

    def create_big_chain(self):
        # Start by creating some coinbases we can spend later
        self.nodes[1].generate(200)
        sync_blocks(self.nodes[0:2])
        self.nodes[0].generate(150)
        # Then mine enough full blocks to create more than 2200MiB of data
        mine_large_blocks(self.nodes[0], 2395)
        sync_blocks(self.nodes[0:2])
        # Note: Separated the manual testing from the main test
        # This can and should be improved in the future
        mine_large_blocks(self.nodes[3], 995)
        mine_large_blocks(self.nodes[4], 995)

    def test_height_min(self):
        if not os.path.isfile(self.prunedir+"blk00000.dat"):
            raise AssertionError("blk00000.dat is missing, pruning too early")
        print("Success")
        print("Though we're already using more than 2200MiB, current usage:", calc_usage(self.prunedir))
        print("Mining 20 more blocks should cause the first block file to be pruned")
        # Pruning doesn't run until we're allocating another chunk, 20 full blocks past the height cutoff will ensure this
        mine_large_blocks(self.nodes[0], 20)

        waitstart = time.time()
        while os.path.isfile(self.prunedir+"blk00000.dat"):
            time.sleep(0.1)
            if time.time() - waitstart > 30:
                raise AssertionError("blk00000.dat not pruned when it should be")

        print("Success")
        usage = calc_usage(self.prunedir)
        print("Usage should be below target:", usage)
        if (usage > 2200):
            raise AssertionError("Pruning target not being met")

    def create_chain_with_staleblocks(self):
        # Create stale blocks in manageable sized chunks
        print("Mine 24 (stale) blocks on Node 1, followed by 25 (main chain) block reorg from Node 0, for 12 rounds")
        for j in range(12):
            # Disconnect node 0 so it can mine a longer reorg chain without knowing about node 1's soon-to-be-stale chain
            # Node 2 stays connected, so it hears about the stale blocks and then reorg's when node0 reconnects
            # Stopping node 0 also clears its mempool, so it doesn't have node1's transactions to accidentally mine
            self.stop_node(0)
            self.nodes[0]=start_node(0, self.options.tmpdir, ["-debug","-maxreceivebuffer=20000", "-checkblocks=6"], timewait=1200)
           
            # Mine 24 blocks in node 1
            mine_large_blocks(self.nodes[1], 24)

            # Reorg back with 25 block chain from node 0
            mine_large_blocks(self.nodes[0], 25)

            # Create connections in the order so both nodes can see the reorg at the same time
            connect_nodes(self.nodes[1], 0)
            connect_nodes(self.nodes[2], 0)
            sync_blocks(self.nodes[0:3])

        print("Usage can be over target because of high stale rate:", calc_usage(self.prunedir))

    def reorg_test(self):
        # Node 1 will mine a 1441 block chain starting 1439 blocks back from Node 0 and Node 2's tip
        # This will cause Node 2 to do a reorg requiring 1440 blocks of undo data to the reorg_test chain
        # Reboot node 1 to clear its mempool (hopefully make the invalidate faster)
        # Lower the block max size so we don't keep mining all our big mempool transactions (from disconnected blocks)
        self.stop_node(1)
        self.nodes[1]=start_node(1, self.options.tmpdir, ["-debug", "-maxreceivebuffer=20000", "-blockmaxsize=5000", "-blockmaxweight=20000", "-checkblocks=6", "-disablesafemode"], timewait=1200)

        height = self.nodes[1].getblockcount()
        print("Current block height:", height)

        invalidheight = height-1439
        badhash = self.nodes[1].getblockhash(invalidheight)
        print("Invalidating block at height:",invalidheight,badhash)
        self.nodes[1].invalidateblock(badhash)

        # We've now switched to our previously mined-24 block fork on node 1, but that's not what we want
        # So invalidate that fork as well, until we're on the same chain as node 0/2 (but at an ancestor 1440 blocks ago)
        mainchainhash = self.nodes[0].getblockhash(invalidheight - 1)
        curhash = self.nodes[1].getblockhash(invalidheight - 1)
        print('curhash != mainchainhash: ', curhash != mainchainhash)
        while curhash != mainchainhash:
            self.nodes[1].invalidateblock(curhash)
            curhash = self.nodes[1].getblockhash(invalidheight - 1)

        assert(self.nodes[1].getblockcount() == invalidheight - 1)
        print("New best height", self.nodes[1].getblockcount())

        # Reboot node1 to clear those giant tx's from mempool
        self.stop_node(1)
        self.nodes[1]=start_node(1, self.options.tmpdir, ["-debug","-maxreceivebuffer=20000", "-blockmaxsize=5000", "-blockmaxweight=20000", "-checkblocks=6", "-disablesafemode"], timewait=1200)

        print("Generating new longer chain of 1441 more blocks")
        self.nodes[1].generate(1441)

        print("Reconnect nodes")
        connect_nodes(self.nodes[0], 1)
        connect_nodes(self.nodes[2], 1)
        sync_blocks(self.nodes[0:3], timeout=300)

        print("Verify height on node 2:",self.nodes[2].getblockcount())
        print("Usage possibly still high bc of stale blocks in block files:", calc_usage(self.prunedir))

        print("Mine 992 more blocks so we have requisite history (some blocks will be big and cause pruning of previous chain)")
        # Get node0's wallet transactions back in its mempool, to avoid the
        # mined blocks from being too small.
        self.nodes[0].resendwallettransactions()
        mine_large_blocks(self.nodes[0], 992)

        sync_blocks(self.nodes[0:3], timeout=120)

        usage = calc_usage(self.prunedir)
        print("Usage should be below target:", usage)
        if (usage > 2200):
            raise AssertionError("Pruning target not being met")

        return invalidheight, badhash

    def reorg_back(self):
        # Verify that a block on the old main chain fork has been pruned away
        assert_raises_jsonrpc(-1, "Block not available (pruned data)", self.nodes[2].getblock, self.forkhash)
        print("Will need to redownload block",self.forkheight)

        # Verify that we have enough history to reorg back to the fork point
        # Although this is more than 1440 blocks, because this chain was written more recently
        # and only its other 1441 small and 992 large block are in the block files after it,
        # its expected to still be retained
        self.nodes[2].getblock(self.nodes[2].getblockhash(self.forkheight))

        first_reorg_height = self.nodes[2].getblockcount()
        curchainhash = self.nodes[2].getblockhash(self.mainchainheight)
        self.nodes[2].invalidateblock(curchainhash)
        goalbestheight = self.mainchainheight
        goalbesthash = self.mainchainhash2

        # As of 0.10 the current block download logic is not able to reorg to the original chain created in
        # create_chain_with_stale_blocks because it doesn't know of any peer that's on that chain from which to
        # redownload its missing blocks.
        # Invalidate the reorg_test chain in node 0 as well, it can successfully switch to the original chain
        # because it has all the block data.
        # However it must mine enough blocks to have a more work chain than the reorg_test chain in order
        # to trigger node 2's block download logic.
        # At this point node 2 is within 1440 blocks of the fork point so it will preserve its ability to reorg
        if self.nodes[2].getblockcount() < self.mainchainheight:
            blocks_to_mine = first_reorg_height + 1 - self.mainchainheight
            print("Rewind node 0 to prev main chain to mine longer chain to trigger redownload. Blocks needed:", blocks_to_mine)
            self.nodes[0].invalidateblock(curchainhash)
            assert(self.nodes[0].getblockcount() == self.mainchainheight)
            assert(self.nodes[0].getbestblockhash() == self.mainchainhash2)
            goalbesthash = self.nodes[0].generate(blocks_to_mine)[-1]
            goalbestheight = first_reorg_height + 1

        print("Verify node 2 reorged back to the main chain, some blocks of which it had to redownload")
        waitstart = time.time()
        while self.nodes[2].getblockcount() < goalbestheight:
            time.sleep(0.1)
            if time.time() - waitstart > 900:
                raise AssertionError("Node 2 didn't reorg to proper height")
        assert(self.nodes[2].getbestblockhash() == goalbesthash)
        # Verify we can now have the data for a block previously pruned
        assert(self.nodes[2].getblock(self.forkhash)["height"] == self.forkheight)

    def manual_test(self, node_number, use_timestamp):
        # at this point, node has 995 blocks and has not yet run in prune mode
        node = self.nodes[node_number] = start_node(node_number, self.options.tmpdir, ["-debug=0"], timewait=900)
        assert_equal(node.getblockcount(), 995)
        assert_raises_jsonrpc(-1, "not in prune mode", node.pruneblockchain, 500)
        self.stop_node(node_number)

        # now re-start in manual pruning mode
        node = self.nodes[node_number] = start_node(node_number, self.options.tmpdir, ["-debug=0","-prune=1"], timewait=900)
        assert_equal(node.getblockcount(), 995)

        def height(index):
            if use_timestamp:
                return node.getblockheader(node.getblockhash(index))["time"] + RESCAN_WINDOW
            else:
                return index

        def prune(index, expected_ret=None):
            ret = node.pruneblockchain(height(index))
            # Check the return value. When use_timestamp is True, just check
            # that the return value is less than or equal to the expected
            # value, because when more than one block is generated per second,
            # a timestamp will not be granular enough to uniquely identify an
            # individual block.
            if expected_ret is None:
                expected_ret = index
            if use_timestamp:
                assert_greater_than(ret, 0)
                assert_greater_than(expected_ret + 1, ret)
            else:
                assert_equal(ret, expected_ret)

        def has_block(index):
            return os.path.isfile(self.options.tmpdir + "/node{}/regtest/blocks/blk{:05}.dat".format(node_number, index))

        # should not prune because chain tip of node 3 (995) < PruneAfterHeight (1000)
        assert_raises_jsonrpc(-1, "Blockchain is too short for pruning", node.pruneblockchain, height(500))

        # mine 6 blocks so we are at height 1001 (i.e., above PruneAfterHeight)
        node.generate(6)
        assert_equal(node.getblockchaininfo()["blocks"], 1001)

        # negative heights should raise an exception
        assert_raises_jsonrpc(-8, "Negative", node.pruneblockchain, -10)

        # height=100 too low to prune first block file so this is a no-op
        prune(100)
        if not has_block(0):
            raise AssertionError("blk00000.dat is missing when should still be there")

        # Does nothing
        node.pruneblockchain(height(0))
        if not has_block(0):
            raise AssertionError("blk00000.dat is missing when should still be there")

        # height=141 should prune first file
        prune(141)
        if has_block(0):
            raise AssertionError("blk00000.dat is still there, should be pruned by now")
        if not has_block(1):
            raise AssertionError("blk00001.dat is missing when should still be there")

        # height=282 should prune second file
        prune(282)
        if has_block(1):
            raise AssertionError("blk00001.dat is still there, should be pruned by now")

        # height=1000 should not prune anything more, because tip-288 is in blk00002.dat.
        prune(1000)
        if has_block(2):
            raise AssertionError("blk00002.dat is still there, should be pruned by now")

        # advance the tip so blk00002.dat and blk00003.dat can be pruned (the last 288 blocks should now be in blk00004.dat)
        node.generate(288)
        prune(1000)

        for fnum in range(7):
            if has_block(fnum):
                raise AssertionError(f"blk0000{fnum}.dat is still there, should be pruned by now")
        if not has_block(7):
            raise AssertionError("blk00007.dat is missing when should still be there")        

        # stop node, start back up with auto-prune at 2200MB, make sure still runs
        self.stop_node(node_number)
        self.nodes[node_number] = start_node(node_number, self.options.tmpdir, ["-debug=0","-prune=2200"], timewait=900)

        print("Success")

    def wallet_test(self):
        # check that the pruning node's wallet is still in good shape
        print("Stop and start pruning node to trigger wallet rescan")
        self.stop_node(2)
        start_node(2, self.options.tmpdir, ["-debug=1","-prune=2200"])
        print("Success")

        # check that wallet loads successfully when restarting a pruned node after IBD.
        # this was reported to fail in #7494.
        print ("Syncing node 5 to test wallet")
        connect_nodes(self.nodes[0], 5)
        nds = [self.nodes[0], self.nodes[5]]
        sync_blocks(nds, wait=5, timeout=300)
        self.stop_node(5) #stop and start to trigger rescan
        start_node(5, self.options.tmpdir, ["-debug=1","-prune=2200"])
        print ("Success")

    def run_test(self):
        print("Warning! This test requires 21GB of disk space and takes over 20 mins (up to 2 hours)")
        print("Mining a big blockchain of 2745 blocks")
        self.create_big_chain()
        # Chain diagram key:
        # *   blocks on main chain
        # +,&,$,@ blocks on other forks
        # X   invalidated block
        # N1  Node 1
        #
        # Start by mining a simple chain that nodes 0-2 have
        # N0=N1=N2 **...*(2745)

        # stop manual-pruning nodes with 995 blocks
        self.stop_node(3)
        self.stop_node(4)

        print("Check that we haven't started pruning yet because we're below PruneAfterHeight")
        self.test_height_min()
        # Extend this chain past the PruneAfterHeight
        # N0=N1=N2 **...*(2765)

        print("Check that we'll exceed disk space target if we have a very high stale block rate")
        self.create_chain_with_staleblocks()
        # Disconnect N0
        # And mine a 24 block chain on N1 and a separate 25 block chain on N0
        # N1=N2 **...*+...+(2789)
        # N0    **...**...**(2790)
        #
        # reconnect nodes causing reorg on N1 and N2
        # N1=N2 **...*(2765) *...**(2790)
        #                   \
        #                    +...+(2789)
        #
        # repeat this process until you have 12 stale forks hanging off the
        # main chain on N1 and N2
        # N0    *************************...***************************(3065)
        #
        # N1=N2 **...*(2765) *...**(2790) *..         ..**(3040) *...**(3065)
        #                   \            \                      \
        #                    +...+(2789)  &..                    $...$(3064)

        # Save some current chain state for later use
        self.mainchainheight = self.nodes[2].getblockcount()   #3065
        self.mainchainhash2 = self.nodes[2].getblockhash(self.mainchainheight)

        print("Check that we can survive a 1440 block reorg still")
        (self.forkheight,self.forkhash) = self.reorg_test() #(1626, )
        # Now create a 1440 block reorg by mining a longer chain on N1
        # First disconnect N1
        # Then invalidate 1626 on main chain and 1625 on fork so height is 1625 on main chain
        # N1   **...*(2765) **...**(1625)X..
        #                  \
        #                   ++...+(1624)X..
        #
        # Now mine 1441 more blocks on N1
        # N1    **...*(2765) **...**(1625) @@...@(3066)
        #                 \               \
        #                  \               X...
        #                   \                 \
        #                    ++...+(1624)X..   ..
        #
        # Reconnect nodes and mine 992 more blocks on N1
        # N1    **...*(2765) **...**(1625) @@...@@@(4058)
        #                 \               \
        #                  \               X...
        #                   \                 \
        #                    ++...+(1624)X..   ..
        #
        # N2    **...*(2765) **...**(1625) @@...@@@(4058)
        #                 \               \
        #                  \               *...**(3065)
        #                   \                 \
        #                    ++...++(2789)     ..
        #
        # N0    ********************(1625) @@...@@@(4058)
        #                                 \
        #                                  *...**(3065)

        print("Test that we can rerequest a block we previously pruned if needed for a reorg")
        self.reorg_back()
        # Verify that N2 still has block 1626 on current chain (@), but not on main chain (*)
        # Invalidate 1626 on current chain (@) on N2 and we should be able to reorg to
        # original main chain (*), but will require redownload of some blocks
        # In order to have a peer we think we can download from, must also perform this invalidation
        # on N0 and mine a new longest chain to trigger.
        # Final result:
        # N0    ********************(1625) **...****(4059)
        #                                 \
        #                                  X@...@@@(4058)
        #
        # N2    **...*(2765) **...**(1625) **...****(4059)
        #                 \               \
        #                  \               X@...@@@(4058)
        #                   \
        #                    +..
        #
        # N1 doesn't change because 1626 on main chain (*) is invalid

        print("Test manual pruning with block indices")
        self.manual_test(3, use_timestamp=False)

        print("Test manual pruning with timestamps")
        self.manual_test(4, use_timestamp=True)

        print("Test wallet re-scan")
        self.wallet_test()

        print("Done")

if __name__ == '__main__':
    PruneTest().main()
