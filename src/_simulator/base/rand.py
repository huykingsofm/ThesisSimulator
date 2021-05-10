import random


class Rand(object):
    @staticmethod
    def randbytes(key, size):
        random.seed(key)

        random_list = []
        for _ in range(size):
            random_list.append(random.randint(0, 255))

        return bytes(random_list)

    @staticmethod
    def randperm(key, low, high):
        random.seed(key)
        return random.sample(range(low, high + 1), high - low + 1)
