# -*- coding: utf-8 -*-
# Exercise 3.3 大寫字母循環排列
# 知識點 id: q3_3  |  參考解答 (非講義原文)

letters = 'ABCDEFGHIJ'
for i in range(10):
    for j in range(10):
        print(letters[(i + j) % 10], end='')
    print()

# 另解：切片
for i in range(10):
    print(letters[i:] + letters[:i])
