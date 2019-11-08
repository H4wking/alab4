import math


class HashTable:
    def __init__(self, hash_type, values):
        self.hash_type = hash_type
        self.values = values
        if self.hash_type == 1:
            self.hash_table = ChainedHashTableDivision(self.values)
        elif self.hash_type == 2:
            self.hash_table = ChainedHashTableMultiplication(self.values)
        elif self.hash_type == 3:
            self.hash_table = OpenAddressingHashTableLinear(self.values)
        elif self.hash_type == 4:
            self.hash_table = OpenAddressingHashTableQuadratic(self.values)
        elif self.hash_type == 5:
            self.hash_table = OpenAddressingHashTableDoubleHashing(self.values)

    def get_collisions_amount(self):
        return self.hash_table.collision_counter

    def find_sum(self, s):
        for el in self.values:
            if self.hash_table.is_in_table(s - el):
                return el, s - el
        return None


class ChainedHashTable:
    def __init__(self, values):
        self.values = values
        self.collision_counter = 0
        self.hash_table = [[] for i in range(len(values))] if math.log(len(values), 2) != int(math.log(len(values), 2))\
                                                           else [[] for i in range(len(values) + 1)]
        self.size = len(self.hash_table)
        self.create_table()

    def h(self, k):
        raise NotImplementedError

    def insert(self, k):
        if self.hash_table[self.h(k)]:
            self.collision_counter += 1
        self.hash_table[self.h(k)].append(k)

    def create_table(self):
        for el in self.values:
            self.insert(el)

    def is_in_table(self, k):
        if k in self.hash_table[self.h(k)]:
            return True
        return False


class ChainedHashTableDivision(ChainedHashTable):
    def h(self, k):
        return k % self.size


class ChainedHashTableMultiplication(ChainedHashTable):
    A = (math.sqrt(5) - 1) / 2

    def h(self, k):
        return int(self.size * ((k * self.A) % 1))


class OpenAddressingHashTable:
    def __init__(self, values):
        self.values = values
        self.collision_counter = 0
        self.hash_table = [None for i in range(len(values) * 3)] if math.log(len(values) * 3, 2) != int(math.log(len(values) * 3, 2))\
                                                             else [None for i in range(len(values) * 3 - 1)]
        self.size = len(self.hash_table)
        self.create_table()

    def h(self, k):
        return k % self.size

    def insert(self, k):
        raise NotImplementedError

    def create_table(self):
        for el in self.values:
            self.insert(el)

    def is_in_table(self, k):
        raise NotImplementedError


class OpenAddressingHashTableLinear(OpenAddressingHashTable):
    def insert(self, k):
        hsh = self.h(k)
        for i in range(self.size):
            if not self.hash_table[(hsh + i) % self.size]:
                self.hash_table[(hsh + i) % self.size] = k
                break
            else:
                self.collision_counter += 1

    def is_in_table(self, k):
        hsh = self.h(k)
        for i in range(self.size):
            if self.hash_table[(hsh + i) % self.size] == k:
                return True
        return False


class OpenAddressingHashTableQuadratic(OpenAddressingHashTable):
    def insert(self, k):
        hsh = self.h(k)
        for i in range(self.size):
            if not self.hash_table[(hsh + i ** 2) % self.size]:
                self.hash_table[(hsh + i ** 2) % self.size] = k
                break
            else:
                self.collision_counter += 1

    def is_in_table(self, k):
        hsh = self.h(k)
        for i in range(self.size):
            if self.hash_table[(hsh + i ** 2) % self.size] == k:
                return True
        return False


class OpenAddressingHashTableDoubleHashing(OpenAddressingHashTable):
    def h2(self, k):
        return 5 - (k % 5)

    def insert(self, k):
        hsh = self.h(k)
        hsh2 = self.h2(k)
        for i in range(self.size):
            if not self.hash_table[(hsh + i * hsh2) % self.size]:
                self.hash_table[(hsh + i * hsh2) % self.size] = k
                break
            else:
                self.collision_counter += 1

    def is_in_table(self, k):
        hsh = self.h(k)
        hsh2 = self.h2(k)
        for i in range(self.size):
            if self.hash_table[(hsh + i * hsh2) % self.size] == k:
                return True
        return False
