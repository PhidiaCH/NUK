# -*- coding: utf-8 -*-
# 範例：黃金比例 (Golden Ratio)
# 知識點 id: ex_golden  |  講義程式

from decimal import Decimal, getcontext
getcontext().prec = 50   # 設定最大有效位數
n = 30                   # 精確至小數點後第 30 位

a, b, count = 1, 1, 0
# < Method 1 > : count = 73 for n = 30
# while (round(Decimal(str(1+a/b)),n) - round(Decimal(str(b/a)),n)) != 0:
# < Method 2 > : count = 74 for n = 30
while abs(Decimal(str(1+a/b))/Decimal(str(b/a)) - Decimal('1.0')) > 0.1**(n+1):
    a, b, count = Decimal(str(b)), Decimal(str(a+b)), count+1

print('n = ', n, ' count = ', count, ': \t a =', a, '\t b =', b)
print('精確至第', n, '位數 :\t b/a = \t', Decimal(str(b/a)))
print('精確至第', n, '位數 :\t (a+b)/b = \t', Decimal(str(1+a/b)))
print('精確至第 50 位數 : Correct Answer = \t',
      Decimal('1.61803398874989484820458683436563811772030917980576'))
