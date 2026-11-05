# -*- coding: utf-8 -*-
# Dictionary Comprehension
# 知識點 id: c_dict_comp  |  講義程式

q = {}
for x in range(0, 6):
    q[x] = x**2 + 2*x + 1
print(q)
q = {x: x**2 + 2*x + 1 for x in range(0, 6)}
print(q)   # {0: 1, 1: 4, 2: 9, 3: 16, 4: 25, 5: 36}
