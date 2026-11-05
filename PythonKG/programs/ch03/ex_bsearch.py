# -*- coding: utf-8 -*-
# 範例：二元搜尋法求平方根
# 知識點 id: ex_bsearch  |  講義程式
# 範例輸入: 2

from math import trunc
from decimal import Decimal, getcontext
getcontext().prec = 31   # 最大精度至小數點後第 30 位
n = 25                   # 問題精度：小數點後第 25 位

a = float(input("Enter a positive number: "))
if a < 0:
    raise ValueError(' **** a = %s : < 0: ERROR !! ' % a)

lower, upper = 0, a
if a < 1: upper = 1

while round(Decimal(str(upper)), n) != round(Decimal(str(lower)), n):
    avg = (Decimal(str(upper)) + Decimal(str(lower))) / Decimal('2')
    if avg**2 >= Decimal(str(a)):
        upper = avg
    else:
        lower = avg

sol = Decimal(str(trunc(upper * 10**n))) / Decimal(str(10**n))
print(' Upper of Square Root =', upper)
print(' Lower of Square Root =', lower)
print(a, '的平方根，精確至小數點後第', n, '位 :')
print(' squareRoot(', a, ') =', sol)
# squareRoot( 2.0 ) = 1.4142135623730950488016887
