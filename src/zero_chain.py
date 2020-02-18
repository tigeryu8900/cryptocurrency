
import requests
from src import transaction
from src.zero_merkle import ZeroMerkleTree
from src.util import JsonSerializable, Hasher


class BlockHeader(JsonSerializable):
    def __init__(self, height: int, previous_hash: str, transaction_root: str, difficulty: int=2, nonce: int=0):
        self.height = height
        self.previous_hash = previous_hash
        self.transaction_root = transaction_root
        self.nonce = nonce
        self.difficulty = difficulty  # the default difficulty is 2


class ZeroChain(object):
    def __init__(self):
        self.new_transactions = []
        self.block_headers = []
        self.transactions = []
        self.difficulty = 2  # pow difficulty level
        self.nodes = set()  # nodes in the network

        # Create the genesis block
        block_head = BlockHeader(0, "", "", self.difficulty)
        self.pow_add_block(block_head)

    def pow_add_block(self, block_header):
        """
        Run one round of pow to get a valid block and add to chain.
        """

        # run pow
        while self.proof_pow(block_header) is False:
            block_header.nonce += 1

        self.block_headers.append(block_header)
        self.transactions.append(self.new_transactions)
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
        block_header = BlockHeader(height = self.block_height,
                                   previous_hash = Hasher.object_hash(self.latest_block),
                                   transaction_root = transaction_root,
                                   difficulty = self.difficulty,
                                   nonce = 0)
        self.pow_add_block(block_header)
        return block_header

    @staticmethod
    def proof_pow(block_header):
        """
        Validates the block_header
        :param block_header:
        :returns True if the block_header is a valid pow.
        """
        difficulty = block_header.difficulty
        return Hasher.object_hash(block_header)[:difficulty] == "0" * difficulty

    def transfer(self, sender, receiver, amount):
        """
        Creates a transfer transaction and added to the new transaction pool.
        :returns the created transaction
        """

        print(sender, receiver, amount)
        txn = transaction.TransferTxn(sender, receiver, amount)
        self.new_transactions.append(txn)
        return txn

    def sync(self):
        """
        Sync with other nodes in the network, replace current chain with
        the longest valid chain in the network
        :return: True if current chain is replaced otherwise False
        """
        newchain = None
        longest_node = None
        # find the longest node in the network
        for node in self.nodes:
            response = requests.get(f"http://{node}/status")

            if response.status_code == 200:
                block_height = response.json()["block_height"]
                if block_height > self.block_height:
                    longest_node = node

        if longest_node is None:
            # this node is already the longest node
            return False

        # sync with the longest node
        response = requests.get(f"http://{longest_node}/fullnode")
        if response.status_code == 200:
            block_height = response.json()["block_height"]
            block_headers = response.json()["block_headers"]
            transactions = response.json()["transactions"]

            # sanity check
            if block_height > self.block_height and \
                    block_height == len(block_headers) and \
                    len(block_headers) == len(transactions):
                # replace current node
                self.block_headers = [BlockHeader.from_json(b) for b in block_headers]
                # we may need to take care of other types of transactions later
                self.transactions = [[transaction.TransferTxn.from_json(t) for t in tx] for tx in transactions]
                return True

        # the longest node is not sound
        return False


    @staticmethod
    def verify_chain(block_headers: list, transactions: list):
        """
        Verify if a given chain is valid.
        :param block_headers: list of block headers
        :param transactions: list of transactions of each block
        :return: True if the given chain is valid
        """
        if len(block_headers) != len(transactions) or len(block_headers) < 1:
            return False

        # validate the all the rest of blocks
        for i in range(len(block_headers)):
            # check if the block links to the previous block except the genesis block
            if i > 0:
                if block_headers[i].previous_hash != Hasher.object_hash(block_headers[i-1]):
                    return False

            # create transaction merkle tree and get the root
            if block_headers[i].transaction_root != ZeroMerkleTree(transactions[i]).root_hash:
                return False

            # verify if the proof of work is correct
            if not ZeroChain.proof_pow(block_headers[i]):
                return False

        # return True if all blcoks are fine
        return True


    @property
    def latest_block(self):
        return self.block_headers[-1]

    @property
    def block_height(self):
        return len(self.block_headers)

