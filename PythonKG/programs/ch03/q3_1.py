# -*- coding: utf-8 -*-
# Exercise 3.1 遞減數字三角形
# 知識點 id: q3_1  |  參考解答 (非講義原文)

# for 版本
for n in range(9, 0, -1):
    for k in range(1, n + 1):
        print(k, end='')
    print()

# while 版本
n = 9
while n > 0:
    print(''.join(str(k) for k in range(1, n + 1)))
    n -= 1
