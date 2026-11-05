# -*- coding: utf-8 -*-
# Example 4.3 以 tuple 交換改寫 Fibonacci / GCD / 氣泡排序
# 知識點 id: ex_tuple_algos  |  講義程式

# 費氏數列 (< 1000)
a, b = 0, 1
while b < 1000:
    print(b, end=' ')
    a, b = b, a+b              # (a, b) = (b, a+b)
print()

# GCD
a, b = 21, 144
while a != 0:
    a, b = b % a, a            # (a, b) = (b % a, a)
print('GCD =', b)

# 氣泡排序
fruits = ['banana', 'apple', 'pineapple', 'watermelon', 'cherry']
for _ in fruits:
    for i in range(len(fruits)-1):
        if fruits[i] > fruits[i+1]:
            fruits[i], fruits[i+1] = fruits[i+1], fruits[i]
print(fruits)
