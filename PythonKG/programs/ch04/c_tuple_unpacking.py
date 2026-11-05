# -*- coding: utf-8 -*-
# tuple packing / unpacking 與交換
# 知識點 id: c_tuple_unpacking  |  講義程式

t1 = (('ABC', 'NBC', 'CBS'), ('Python', 123, 3.1416), (2.71828, 1.732))
tv, py, math = t1
print(tv); print(py); print(math)
a, b = 1, 2
a, b = b, a        # swap
print(a, b)
