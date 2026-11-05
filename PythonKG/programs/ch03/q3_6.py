# -*- coding: utf-8 -*-
# Exercise 3.6 樂透選號 + 氣泡排序
# 知識點 id: q3_6  |  參考解答 (非講義原文)

from random import random

def lotto_pick(k=6, lo=1, hi=49):
    pool = list(range(lo, hi + 1))
    picks = []
    for _ in range(k):
        idx = int(random() * 10000) % len(pool)
        picks.append(pool.pop(idx))     # 取出並移除
    return picks

def bubble_sort(a):
    a = a[:]
    for _ in range(len(a)):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
    return a

nums = lotto_pick()
print('電腦選號 :', nums)
print('排序後   :', bubble_sort(nums))
