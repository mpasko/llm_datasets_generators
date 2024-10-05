from functools import reduce
import random

class Sampler:
    def __init__(self, formatter, dimensions, sparcity):
        self.dimensions = dimensions
        self.formatter = formatter
        self.sparcity = sparcity

    def sample(self):
        total = reduce(lambda x, y: x*y, self.dimensions)
        for next in range(0, total):
            indexes = self.split(next, self.dimensions)
            sparse_indexes = [self.extend(index, sparse) for index, sparse in zip(indexes, self.sparcity)]
            formatted = self.formatter(sparse_indexes)
            print(formatted)

    def extend(self, index, sparcity):
        return random.randrange(index*sparcity, (index+1)*sparcity)

    def split(self, number, dimensions):
        sub_indexes = []
        rest = number
        for dimension in dimensions:
            sub_indexes.append(rest % dimension)
            rest = int(rest / dimension)
        return sub_indexes