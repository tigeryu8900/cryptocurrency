
import transaction
from zero_merkle import ZeroMerkleTree
from util import JsonSerializable, Hasher


class BlockHeader(JsonSerializable):
    def __init__(self, height: int, previous_hash: str, transaction_root: str, nonce: str):
        self.height = height
        self.previous_hash = previous_hash
        self.transacton_root = transaction_root
        self.nonce = nonce


class ZeroChain(object):
    def __init__(self):
        self.new_transactions = []
        self.block_headers = []
        self.transactions = []
        self.difficulty = 4  # pow difficulty level

        # Create the genesis block
        block_head = BlockHeader(height = 0, previous_hash="", transaction_root = "", nonce = 0)
        self.pow_add_block(block_head)

    def pow_add_block(self, block_header):
        """
        Run one round of pow to get a valid block and add to chain.
        """

        # run pow
        while self.proof_pow(block_header) is False:
            block_header.nonce += 1

        self.block_headers.append(block_header)
        self.transactions.append(self.transactions)
        # Clear new transaction list
        self.new_transactions = []


    def create_block(self):
        """
        Creates a block and include all transactions in self.new_transactions.
        :returns the new created block_header
        """

        # create transaction merkle tree and get the root
        transaction_tree = ZeroMerkleTree(self.new_transactions)
        transaction_root = transaction_tree.root_hash
        block_header = BlockHeader(height = self.block_height + 1,
                                   previous_hash = Hasher.object_hash(self.latest_block),
                                   transaction_root = transaction_root,
                                   nonce = 0)
        self.pow_add_block(block_header)
        return block_header


    def proof_pow(self, block_header):
        """
        Validates the block_header
        :param block_header:
        :return: True if the block_header is a valid pow.
        """
        return Hasher.object_hash(block_header)[:4] == "0" * self.difficulty

    def transfer(self, sender, receiver, amount):
        """
        Creates a transfer transaction and added to the new transaction pool.
        """
        self.new_transactions.append(transaction.TransferTxn(sender, receiver, amount))

    @property
    def latest_block(self):
        return self.block_headers[-1]

    @property
    def block_height(self):
        return len(self.block_headers)

