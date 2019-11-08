import random
import time
from sum_of_two import HashTable


a = list(range(100000))
random.shuffle(a)
s = time.time()
c = HashTable(5, a)
print(c.find_sum(10000))
print(time.time() - s)
