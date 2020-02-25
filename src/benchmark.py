
#import math
import random
import string
import statistics
import time
import gc
from src.zero_merkle import ZeroMerkleTree, BitcoinMerkleTree, LibraMerkleTree


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
                               string.digits, k = data_size)))
    return res


def test_algorithm(data: list, round: int, algorithm):
    """ perform a round of performance test for the given algorithm """
    numbers = []
    for r in range(round):
        gc.collect()
        gc.freeze()
        gc.disable()
        t0 = time.time()
        algorithm(data)
        gc.enable()
        gc.unfreeze()
        t1 = time.time()
        numbers.append((t1 - t0) * 1000)

    return [statistics.mean(numbers)]
    #return [statistics.median(numbers), statistics.mean(numbers), statistics.stdev(numbers)]

def test_all_algorithms(data_size: int, data_count: int, round: int, algorithms: list):
    data = generate_data(data_size, data_count)
    for a in algorithms:
        times = test_algorithm(data, round, a)
        print(f"{data_size},{a.__name__},{times}")


if __name__ == "__main__":
    #gc.disable()
    algorithms = [BitcoinMerkleTree, LibraMerkleTree, ZeroMerkleTree]
    test_all_algorithms(128, (1 << 10) + 1, 400, algorithms)
