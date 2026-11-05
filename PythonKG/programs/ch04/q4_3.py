# -*- coding: utf-8 -*-
# Exercise 4.3 以 list comprehension 改寫 pairs
# 知識點 id: q4_3  |  參考解答 (非講義原文)

pairs = [(i, j, (i + j) / 2) for i in [1, 3, 5] for j in [4, 1, 2] if i != j]
print(pairs)
