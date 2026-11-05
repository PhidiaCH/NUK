# -*- coding: utf-8 -*-
# Exercise 5.4 質數存入 dict {index: prime}
# 知識點 id: q5_4  |  參考解答 (非講義原文)
# 範例輸入: 50

N = int(input('N = '))
primes = [n for n in range(2, N)
          if all(n % x for x in range(2, int(n ** 0.5) + 1))]
prime_dict = {i: p for i, p in enumerate(primes)}
print(prime_dict)
