# -*- coding: utf-8 -*-
# 範例：費氏數列 Fibonacci
# 知識點 id: ex_fib  |  講義程式

a, b = 0, 1
print('Fibonacci numbers = ', a, end=' ')
while b < 50:
    print(b, end=' ')
    a, b = b, a+b
# 0 1 1 2 3 5 8 13 21 34
