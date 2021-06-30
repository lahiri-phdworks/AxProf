import sys
import os
import random
import string

entries = 10

if __name__ == "__main__":
    for i in range(100):
        with open(f"countminsketch_{i}.txt", mode="w") as fileptr:
            fileptr.write(f"{entries}\n")
            fileptr.write(f"{random.randint(0, entries - 1)}\n")
            fileptr.write(f"{random.randint(0, entries - 1)}\n")
            fileptr.write(f"{random.randint(0, entries - 1)}\n")
            fileptr.write(f"{random.randint(0, 100)}\n")
            fileptr.write(f"{random.randint(0, 100)}\n")
            fileptr.write(f"{random.randint(0, 100)}\n")
            fileptr.write(f"{random.randint(0, 100)}\n")
            for j in range(entries):
                strings = ''.join(random.SystemRandom().choice(
                    string.ascii_uppercase + string.digits) for _ in range(15))
                fileptr.write(f"{strings}\n")
