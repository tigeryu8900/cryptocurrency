
import copy
from src.util import Hasher

class MerkleNode:
    def __init__(self, left, right, hash: str = None):
        self.left = left
        self.right = right
        if hash is None and left is not None and right is not None:
            self.hash = Hasher.hash(left.hash + right.hash)
        else:
            self.hash = hash


class ZeroMerkleTree:
    def __init__(self, items: list, size = None):
        self.number_of_nodes = 0
        self.number_of_hashs = 0
        self.root = self.construct(items, size)

    @property
    def root_hash(self):
        return self.root.hash

    def construct(self, items: list, size):
        if size is None:
            size = len(items)
        layer = [MerkleNode(None, None, Hasher.object_hash(items[x])) for x in range(size)]

        self.number_of_nodes += len(layer)
        self.number_of_hashs += len(layer)

        while len(layer) > 1:
            up_layer = []
            for i in range(0, len(layer) - 1, 2):
                up_layer.append(MerkleNode(layer[i], layer[i + 1]))
            if len(layer) & 1 == 1:  # move the last odd item to the upper layer
                up_layer.append(layer[-1])
            self.number_of_nodes += int(len(layer) / 2)
            self.number_of_hashs += int(len(layer) / 2)
            layer = up_layer

        # return the root
        if len(layer) == 1:
            return layer[0]
        else:
            self.number_of_nodes += 1
            return MerkleNode(None, None, "")


class BitcoinMerkleTree:
    def __init__(self, items: list, size = None):
        self.number_of_nodes = 0
        self.number_of_hashs = 0
        self.root = self.construct(items, size)

    @property
    def root_hash(self):
        return self.root.hash

    def construct(self, items: list, size):
        if size is None:
            size = len(items)
        layer = [MerkleNode(None, None, Hasher.object_hash(items[x])) for x in range(size)]
        self.number_of_nodes += len(layer)
        self.number_of_hashs += len(layer)

        while len(layer) > 1:
            if len(layer) & 1 == 1:  # duplicate the last odd item
                #layer.append(copy.copy(layer[-1]))
                layer.append(MerkleNode(None, None, layer[-1].hash))
                self.number_of_nodes += 1

            up_layer = []
            for i in range(0, len(layer) - 1, 2):
                up_layer.append(MerkleNode(layer[i], layer[i + 1]))
            self.number_of_nodes += int(len(layer) / 2)
            self.number_of_hashs += int(len(layer) / 2)
            layer = up_layer

        # return the root
        if len(layer) == 1:
            return layer[0]
        else:
            self.number_of_nodes += 1
            return MerkleNode(None, None, "")


class LibraMerkleTree:
    def __init__(self, items: list, size = None):
        self.number_of_nodes = 0
        self.number_of_hashs = 0
        self.root = self.construct(items, size)

    @property
    def root_hash(self):
        return self.root.hash

    def construct(self, items: list, size):
        if size is None:
            size = len(items)
        layer = [MerkleNode(None, None, Hasher.object_hash(items[x])) for x in range(size)]
        self.number_of_nodes += len(layer)
        self.number_of_hashs += len(layer)

        while len(layer) > 1:
            if len(layer) & 1 == 1:  # add an extra null node
                layer.append(MerkleNode(None, None, ""))
                self.number_of_nodes += 1

            up_layer = []
            for i in range(0, len(layer) - 1, 2):
                up_layer.append(MerkleNode(layer[i], layer[i + 1]))
            self.number_of_nodes += int(len(layer) / 2)
            self.number_of_hashs += int(len(layer) / 2)
            layer = up_layer

        # return the root
        if len(layer) == 1:
            return layer[0]
        else:
            self.number_of_nodes += 1
            return MerkleNode(None, None, "")

# The following are Lite Version of merkle trees.

def BitcoinMerkleTreeLite(items: list, size = None):
    if size is None: size = len(items)
    layer = [Hasher.raw_hash(items[x]) for x in range(size)]
    if len(layer) & 1 == 1:
        layer.append(copy.copy(layer[-1]))

    items = len(layer)
    while items > 1:
        if items & 1 == 1:
            layer[items] = copy.copy(layer[items+1])
            items += 1
        for i in range(0, items, 2):
            layer[i>>1] = Hasher.raw_hash(layer[i], layer[i + 1])
        items = (items+1)>>1

    # return the root
    if items == 1:
        return layer[0]
    else:
        return b""


def LibraMerkleTreeLite(items: list, size = None):
    if size is None: size = len(items)
    layer = [Hasher.raw_hash(items[x]) for x in range(size)]
    if len(layer) & 1 == 1:
        layer.append(b"")

    items = len(layer)
    while items > 1:
        if items & 1 == 1:
            layer[items] = b""
            items += 1
        for i in range(0, items, 2):
            layer[i>>1] = Hasher.raw_hash(layer[i], layer[i + 1])
        items = (items+1)>>1

    # return the root
    if items == 1:
        return layer[0]
    else:
        return b""


def ZeroMerkleTreeLite(items: list, size = None):
    if size is None: size = len(items)
    layer = [Hasher.raw_hash(items[x]) for x in range(size)]

    items = len(layer)
    while items > 1:
        for i in range(0, items - 1, 2):
            layer[i>>1] = Hasher.raw_hash(layer[i], layer[i + 1])
        if items & 1 == 1:  # move the last odd item to the upper layer
            layer[(items+1)>>1] = layer[items-1]
        items = (items+1)>>1

    # return the root
    if items == 1:
        return layer[0]
    else:
        return b""
