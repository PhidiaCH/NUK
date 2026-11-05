# -*- coding: utf-8 -*-
# 5.2 frozenset (不可變集合)
# 知識點 id: c_frozenset  |  講義程式

f1 = frozenset([1, 2, 3])
f2 = frozenset([1, 2, 3, 4, 5])
print(f1 < f2, f1 > f2)       # True False
print(f1 & f2, f2 - f1)
print({x for x in f2 if x not in f1})
try:
    f1.add(4)
except AttributeError as e:
    print('AttributeError:', e)
d = {frozenset({'a', 'b'}): 'ok'}   # 可以當 key
print(d)
