# -*- coding: utf-8 -*-
# Example 4.2-7 List Comprehension on Math
# 知識點 id: ex_listcomp_math  |  講義程式

from math import exp, pi
print([str(round(exp(1), i)) for i in range(1, 6)])
# ['2.7', '2.72', '2.718', '2.7183', '2.71828']
print([float(round(pi*10**2, i)) for i in range(1, 6)])
# [314.2, 314.16, 314.159, 314.1593, 314.15927]
