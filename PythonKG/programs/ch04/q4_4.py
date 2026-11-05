# -*- coding: utf-8 -*-
# Exercise 4.4 輸入 N，找出小於 N 的質數
# 知識點 id: q4_4  |  參考解答 (非講義原文)
# 範例輸入: 50

N = int(input('N = '))

# (1) for 迴圈 + for-else
primes = []
for n in range(2, N):
    for x in range(2, int(n ** 0.5) + 1):
        if n % x == 0:
            break
    else:
        primes.append(n)
print(primes)

# (2) list comprehension
primes = [n for n in range(2, N)
          if all(n % x for x in range(2, int(n ** 0.5) + 1))]
print(primes)
