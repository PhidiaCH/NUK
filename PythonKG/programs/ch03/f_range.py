# -*- coding: utf-8 -*-
# range()
# 知識點 id: f_range  |  講義程式

for i in range(2, 10):
    print(i, end=' ')          # 2 3 4 5 6 7 8 9
print()
print(range(5))                # range(0, 5)
print(list(range(5)))          # [0, 1, 2, 3, 4]
print(tuple(range(5)))         # (0, 1, 2, 3, 4)
print(list(range(-15, 25, 3)))
print(list(range(-15, -25, -3)))
