# -*- coding: utf-8 -*-
# 範例：蒙地卡羅法估算圓周率 π
# 知識點 id: ex_montecarlo  |  講義程式

from random import random, seed
from math import sqrt

total = 10**6     # 講義原為 10**8
seed(100)         # 固定亂數種子 => 固定亂數輸出值

i = count = 0
while i < total:
    i += 1
    x, y = random(), random()     # 亂數值介於 [0, 1)
    if sqrt(x**2 + y**2) <= 1.0:  # Euclidean distance
        count += 1

pi = 4 * count / total            # 圓內點數 : 總點數 = π : 4
print('Pi = {:.5f}'.format(pi))
