# -*- coding: utf-8 -*-
# 範例：氣泡排序 Bubble Sort
# 知識點 id: ex_bubble  |  講義程式

fruits = ['banana', 'apple', 'pineapple', 'watermelon', 'cherry']
print('尚未排序的資料：\n', fruits)
for j in fruits:
    for i in range(len(fruits)-1):
        if fruits[i] > fruits[i+1]:
            temp = fruits[i]          # Swapping
            fruits[i] = fruits[i+1]
            fruits[i+1] = temp
print('由小排到大的資料：\n', fruits)
