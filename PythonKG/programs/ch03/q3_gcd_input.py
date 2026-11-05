# -*- coding: utf-8 -*-
# 練習：任意輸入 a, b 計算 GCD 與費氏數列
# 知識點 id: q3_gcd_input  |  參考解答 (非講義原文)
# 範例輸入: 21 / 144 / 100

def gcd(a, b):
    while a != 0:
        a, b = b % a, a
    return abs(b)

def fibonacci(limit):
    a, b, seq = 0, 1, [0]
    while b < limit:
        seq.append(b)
        a, b = b, a + b
    return seq

a = int(input('a = '))
b = int(input('b = '))
print('GCD(%d, %d) = %d' % (a, b, gcd(a, b)))
limit = int(input('費氏數列上限 = '))
print('Fibonacci <', limit, ':', fibonacci(limit))
