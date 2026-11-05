# -*- coding: utf-8 -*-
# 練習：氣泡排序由大排到小
# 知識點 id: q3_bubble_desc  |  參考解答 (非講義原文)

fruits = ['banana', 'apple', 'pineapple', 'watermelon', 'cherry']
for _ in fruits:
    for i in range(len(fruits)-1):
        if fruits[i] < fruits[i+1]:          # 只需把 > 改成 <
            fruits[i], fruits[i+1] = fruits[i+1], fruits[i]
print('由大排到小的資料：', fruits)
