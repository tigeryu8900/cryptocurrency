
import requests
from src import transaction
from src.zero_merkle import ZeroMerkleTree
from src.util import JsonSerializable, Hasher


class BlockHeader(JsonSerializable):
    def __init__(self, height: int, previous_hash: str, transaction_root: str, difficulty: int, nonce: int=0):
        self.height = height
        self.previous_hash = previous_hash
        self.transaction_root = transaction_root
        self.nonce = nonce
        self.difficulty = difficulty  # the default difficulty is 2


class ZeroChain(object):
    def __init__(self):
        self.pending_transactions = []
        self.block_headers = []  # a list of BlockHeader objects, one for each block
        self.transactions = []  # a list of lists of transactions, one nested list for each block
        self.difficulty = 2  # pow difficulty level
        self.nodes = set()  # nodes in the network
        self.node_ipport = ""  # the "ip:port" of this instance

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
        self.transactions.append(self.pending_transactions)
        # Clear new transaction list
        self.pending_transactions = []


    def create_block(self):
        """
        Creates a block and include all transactions in self.pending_transactions.
        :returns the new created block_header
        """

        # create transaction merkle tree and get the root
        transaction_tree = ZeroMerkleTree(self.pending_transactions)
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

        txn = transaction.TransferTxn(sender, receiver, amount)
        self.pending_transactions.append(txn)
        return txn

    # The following are network related functions.

    def add_node(self, new_node: str, propagate: bool):
        """ Adds a new node and propagate to all neighbors if necessary. """
        # skip if the new_node is already added
        if new_node in self.nodes:
            return
        # skip to add self as a neighbor
        if new_node == self.node_ipport:
            return
        # add the new node to the node set
        self.nodes.add(new_node)
        if propagate:
            # then, propagate the new node to all neighbors, set propagate = False to prevent recursive calls
            nodes = [n for n in self.nodes]
            for n in nodes:
                for m in nodes:
                    if not m == n:
                        requests.post(f"http://{n}/register_node", data={"node": m, "propagate": False})
            # finally, add myself to new_node's neighbor list
            requests.post(f"http://{new_node}/register_node", data={"node": self.node_ipport, "propagate": True})


    def sync_self(self):
        """
        Sync with other nodes in the network, replace current chain with
        the longest valid chain in the network
        :return: True if current chain is replaced otherwise False
        """

        longest_node = None
        max_height = 0
        # find the longest node in the network
        for node in self.nodes:
            response = requests.get(f"http://{node}/status")
            if response.status_code == 200:
                block_height = response.json()["block_height"]
                if block_height > self.block_height and block_height > max_height:
                    longest_node = node
                    max_height = block_height

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
                bhs = [BlockHeader.from_json(b) for b in block_headers]
                # we may need to take care of other types of transactions later
                txs = [[transaction.TransferTxn.from_json(t) for t in tx] for tx in transactions]
                if not ZeroChain.verify_chain(bhs, txs):
                    return False  # chain validation fail
                self.block_headers = bhs
                self.transactions = txs
                return True

        # the longest node is not sound
        return False


    def sync(self, propagate):
        # sync this node with neighbors
        replaced = self.sync_self()

        # then, ask all neighbors to sync themselves if necessary
        if propagate:
            for node in self.nodes:
                print(f"ask {node} to sync")
                requests.get(f"http://{node}/sync?propagate=False")
        # return if this node is replaced
        return replaced


    @staticmethod
    def verify_chain(block_headers: list, transactions: list):
        """
        Verify if a given chain is valid.
        :param block_headers: list of block headers
        :param transactions: list of transactions of each block
        :return: True if the given chain is valid
        """
        if len(block_headers) != len(transactions) and len(block_headers) == 0:
            return False

        # an valid chain contains only the genesis block
        if len(block_headers) == 1:
            return True

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

