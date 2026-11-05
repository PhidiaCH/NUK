# -*- coding: utf-8 -*-
# 4.3 tuple 元組 (不可變序列)
# 知識點 id: c_tuple  |  講義程式

t = ();                   print(t)
t = 'Python',;            print(t)        # ('Python',)
t = 'Python', 123, 3.1416;print(t)
t1 = ('ABC', 'NBC', 'CBS'), t, (2.71828, 1.732)   # nested tuple
print(t1)
t2 = ['a', 'b', 'c', 1, 2], [11, 22], ('Python', 3.6)
t2[0].append(3)           # 元素是 list → 可修改 list 本身
print(t2)
try:
    t2[0] = [97, 98, 99]
except TypeError as e:
    print('TypeError:', e)
