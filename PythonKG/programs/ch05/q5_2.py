# -*- coding: utf-8 -*-
# Exercise 5.2 樂透 100 組號碼出現次數統計
# 知識點 id: q5_2  |  參考解答 (非講義原文)

from random import random

def lotto_pick(k=6, lo=1, hi=49):
    pool = list(range(lo, hi + 1))
    return [pool.pop(int(random() * 10000) % len(pool)) for _ in range(k)]

def bubble_sort(a):
    a = a[:]
    for _ in range(len(a)):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
    return a

draws = [bubble_sort(lotto_pick()) for _ in range(100)]
for d in draws[:5]:
    print(d)
print('...')
counts = {n: 0 for n in range(1, 50)}
for d in draws:
    for n in d:
        counts[n] += 1
for n, c in counts.items():
    print('{0:>2d} : {1:>3d}'.format(n, c), end='    ' if n % 5 else '\n')
print('\n總數 =', sum(counts.values()))   # 600
