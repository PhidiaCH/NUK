# -*- coding: utf-8 -*-
# 範例：最大公因數 GCD (輾轉相除法)
# 知識點 id: ex_gcd  |  講義程式

# GCD: greatest common divisor
(a, b) = (21, 144)
while a != 0:
    print(' a =\t', a, '\t b =\t', b)
    a, b = b % a, a
print(" GCD = ", b)
