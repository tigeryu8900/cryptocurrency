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
    def __init__(self, items: list):
        self.root = self.construct(items)

    @property
    def root_hash(self):
        return self.root.hash

    @staticmethod
    def construct(items: list):
        layer = [MerkleNode(None, None, Hasher.object_hash(x)) for x in items]
        while len(layer) > 1:
            up_layer = []
            for i in range(0, len(layer) - 1, 2):
                up_layer.append(MerkleNode(layer[i], layer[i + 1]))
            if len(layer) & 1 == 1:  # move the last odd item to the upper layer
                up_layer.append(layer.pop())
            layer = up_layer

        # return the root
        if len(layer) == 1:
            return layer[0]
        else:
            return MerkleNode(None, None, "")
