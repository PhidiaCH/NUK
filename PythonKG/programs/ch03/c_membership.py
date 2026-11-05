# -*- coding: utf-8 -*-
# 成員運算子 in / not in
# 知識點 id: c_membership  |  講義程式

A = []
for x in [1, 2, 5, 10]:
    if x not in [x*2, 10-x]:
        A.append(x)
print(A)                   # [1, 2, 10]
print('Py' in 'Python')    # True
