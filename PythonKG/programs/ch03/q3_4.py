# -*- coding: utf-8 -*-
# Exercise 3.4 小於 1000 且與 45 互質的自然數
# 知識點 id: q3_4  |  參考解答 (非講義原文)

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return b

coprimes = []
for n in range(1, 1000):
    if gcd(n, 45) == 1:
        coprimes.append(n)
print(coprimes)
print('個數 =', len(coprimes))     # 533
