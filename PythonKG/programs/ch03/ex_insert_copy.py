# -*- coding: utf-8 -*-
# Example 3.2 迴圈中複製並插入元素
# 知識點 id: ex_insert_copy  |  講義程式

fruits = ['apple', 'mango', 'watermelon', 'banana', 'pineapple']
print('fruits (before) =', fruits)
for f in fruits[:]:            # 走訪整個串列的切片複本
    if len(f) <= 8 and len(f) >= 5:
        fruits.insert(4, f)
print('fruits (after) =', fruits)
# ['apple', 'mango', 'watermelon', 'banana', 'banana', 'mango', 'apple', 'pineapple']
