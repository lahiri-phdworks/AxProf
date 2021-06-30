import sys
import os
import random
import string

error = 0.098187
entries = 20

if __name__ == "__main__":
    for i in range(100):
        with open(f"bloomfilter_{i}.txt", mode="w") as fileptr:
            fileptr.write(f"{entries}\n")
            fileptr.write(f"{entries}\n")
            fileptr.write(f"{error}\n")
            fileptr.write(f"{random.randint(0, entries - 1)}\n")
            fileptr.write(f"{random.randint(0, entries - 1)}\n")
            for j in range(entries):
                strings = ''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits) for _ in range(10))
                fileptr.write(f"{strings}\n")
