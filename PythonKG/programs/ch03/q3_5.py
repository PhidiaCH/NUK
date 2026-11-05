# -*- coding: utf-8 -*-
# Exercise 3.5 二元搜尋法求立方根 (正、負、0)
# 知識點 id: q3_5  |  參考解答 (非講義原文)

from decimal import Decimal, getcontext, ROUND_DOWN

def cube_root(a, n=50):
    getcontext().prec = n + 20
    a = Decimal(str(a))
    if a == 0:
        return Decimal(0)
    if a < 0:                          # 負數：利用奇函數性質
        return -cube_root(-a, n)
    lower, upper = Decimal(0), max(a, Decimal(1))
    eps = Decimal(10) ** -(n + 5)
    while upper - lower > eps:
        mid = (lower + upper) / 2
        if mid ** 3 >= a:
            upper = mid
        else:
            lower = mid
    return upper.quantize(Decimal(10) ** -n, rounding=ROUND_DOWN)

for a in (27, 2, 0, -8, -2, 0.001):
    print('cbrt(%s) =' % a, cube_root(a))
