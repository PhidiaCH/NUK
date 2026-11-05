# -*- coding: utf-8 -*-
# Fraction 分數
# 知識點 id: c_fraction  |  講義程式

from fractions import Fraction
from decimal import Decimal
print(Fraction(30, -4))          # -15/2
print(Fraction(2018))            # 2018
print(Fraction())                # 0
print(Fraction('4/23'))          # 4/23
print(Fraction('1.41421'))       # 141421/100000
print(Fraction('-.125'))         # -1/8
print(Fraction('1.7e-3'))        # 17/10000
print(Fraction(3.33))            # 1874623344892969/562949953421312
print(Fraction(Decimal('3.33'))) # 333/100
