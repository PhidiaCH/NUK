# -*- coding: utf-8 -*-
# List Comprehension 串列精簡
# 知識點 id: c_list_comp  |  講義程式

A = [2*n+1 for n in range(1, 10)]
B = [x**2 for x in A if x < 12]
print('A = ', A)   # [3, 5, 7, 9, 11, 13, 15, 17, 19]
print('B = ', B)   # [9, 25, 49, 81, 121]

# 巢狀迴圈 → 一行
pairs = [(i, j) for i in ['Apple', 'Android', 'Asus']
                for j in ['Google', 'Apple', 'Microsoft'] if i != j]
print(pairs)
