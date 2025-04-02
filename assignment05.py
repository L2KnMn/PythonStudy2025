import random

cnts = 0
times = 100000

for i in range(times):
    cnt = 0
    numbers = []

    for num in range(0, 100):
        numbers.append(random.randrange(0, 100))

    for num in range(0, 100):
        if num not in numbers:
            cnt+=1
    cnts += cnt

print(cnts / times)
        