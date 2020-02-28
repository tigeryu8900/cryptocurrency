
import math
import random
import string
import statistics
import time
import timeit
import gc
from src.zero_merkle import ZeroMerkleTree, BitcoinMerkleTree, LibraMerkleTree
from src.zero_merkle import ZeroMerkleTreeLite, BitcoinMerkleTreeLite, LibraMerkleTreeLite
from memory_profiler import profile


def generate_data(data_size: int, data_count: int):
    """
    Generate <count> of strings, each has <data_size> of random characters.
    :param data_size: length of each data string
    :param data_count: number of strings
    :return: the list of string
    """
    res = []
    for i in range(data_count):
        res.append(''.join(random.choices(string.ascii_uppercase +
                               string.digits, k = data_size)).encode())
    return res

def speed_test_repeat(algorithms, data_count, round):
    setup_stm = f"""\
from __main__ import generate_data, BitcoinMerkleTree, LibraMerkleTree, ZeroMerkleTree
from __main__ import generate_data, BitcoinMerkleTree2, LibraMerkleTree2, ZeroMerkleTree2
data = generate_data(15, {data_count})
    """

    print(f"Speed test with {data_count} data items for {round} times")
    for algorithm in algorithms:
        print(algorithm.__name__, timeit.timeit(f"{algorithm.__name__}(data)", setup=setup_stm, number=round)/round*1000)
    print()

def speed_test_random(algorithms, data_count, repeat, round):
    setup_stm = f"""\
from __main__ import generate_data, BitcoinMerkleTree, LibraMerkleTree, ZeroMerkleTree
from __main__ import generate_data, BitcoinMerkleTree2, LibraMerkleTree2, ZeroMerkleTree2
data = generate_data(15, {data_count})
    """

    numbers = {a.__name__:[] for a in algorithms}
    print(f"Speed test with random({data_count}) data items for {round} times")
    for r in range(repeat):
        size = random.randint(data_count>>1, data_count)
        for algorithm in algorithms:
            numbers[algorithm.__name__].append(timeit.timeit(f"{algorithm.__name__}(data, {size})", setup=setup_stm, number=round)/round*1000)
    for algorithm in algorithms:
        print(algorithm.__name__, statistics.mean(numbers[algorithm.__name__]))
    print()


@profile(precision = 6)
def speed_test(algorithms):
    # Test with small number of nodes
    speed_test_repeat(algorithms, (1 << 4), 500)   # best case
    speed_test_repeat(algorithms, (1 << 4)+1, 500) # worse case
    speed_test_random(algorithms, (1 << 4) + 1, 10, 500)  # average case

    # Test with large number of nodes
    speed_test_repeat(algorithms, (1 << 11), 500)   # best case
    speed_test_repeat(algorithms, (1 << 11)+1, 500) # worse case
    speed_test_random(algorithms, (1 << 11) + 1, 10, 500)  # average case


@profile(precision = 6)
def memory_test():
    r = []
    data = generate_data(32, (1<<10) + 1)

    print("Worse case, number_of_nodes, number_of_hashs")
    r.append(BitcoinMerkleTree(data))
    print("BitcoinMerkleTree", r[-1].number_of_nodes, r[-1].number_of_hashs)
    r.append(LibraMerkleTree(data))
    print("LibraMerkleTree", r[-1].number_of_nodes, r[-1].number_of_hashs)
    r.append(ZeroMerkleTree(data))
    print("ZeroMerkleTree", r[-1].number_of_nodes, r[-1].number_of_hashs)
    data.pop()
    print()
    print("Best case, number_of_nodes, number_of_hashs")
    r.append(BitcoinMerkleTree(data))
    print("BitcoinMerkleTree", r[-1].number_of_nodes, r[-1].number_of_hashs)
    r.append(LibraMerkleTree(data))
    print("LibraMerkleTree", r[-1].number_of_nodes, r[-1].number_of_hashs)
    r.append(ZeroMerkleTree(data))
    print("ZeroMerkleTree", r[-1].number_of_nodes, r[-1].number_of_hashs)


if __name__ == "__main__":
    algorithms = [BitcoinMerkleTree, LibraMerkleTree, ZeroMerkleTree]
    # test with Lite version of algorithms
    #algorithms = [BitcoinMerkleTreeLite, LibraMerkleTreeLite, ZeroMerkleTreeLite]

    # run speed tests
    speed_test(algorithms)

    # run memeory usage tests
    gc.collect()
    gc.disable()
    memory_test()