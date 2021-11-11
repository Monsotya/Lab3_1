import os
import timeit
from random import randint

infile = open("text.txt", "a")
while os.stat('text.txt').st_size < 50000000:
    infile.write(str(randint(0, 100)) + "\n")
infile.close()

s = """
with open("text.txt", "r") as f:
    data = f.readlines()
res = 0
for line in data:
    if line.strip().isdigit():
        res += int(line.strip())
"""

print(timeit.timeit(s, number=10))

s = """
res = 0
with open("text.txt", "r") as f:
    for line in f:
        if line.strip().isdigit():
            res += int(line.strip())
"""

print(timeit.timeit(s, number=10))

s = """
with open("text.txt", "r") as f:
    x = (int(line.strip()) for line in f if line.strip().isdigit())
    res = sum(x)
"""

print(timeit.timeit(s, number=10))


