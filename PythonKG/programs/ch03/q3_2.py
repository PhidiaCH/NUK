# -*- coding: utf-8 -*-
# Exercise 3.2 遞增數字三角形
# 知識點 id: q3_2  |  參考解答 (非講義原文)

for n in range(1, 10):
    for k in range(1, n + 1):
        print(k, end='')
    print()

n = 1
while n <= 9:
    print(''.join(str(k) for k in range(1, n + 1)))
    n += 1
