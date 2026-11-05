# -*- coding: utf-8 -*-
# Exercise 4.1 list 方法組合
# 知識點 id: q4_1  |  參考解答 (非講義原文)

w = ['Fly', 'robin', 'fly']
words = ['Fly', 'robin', 'fly', 'Up', 'up', 'to', 'the', 'sky']
words[3:3] = w * 2          # 在索引 3 插入兩份 w (切片指定)
print(words)

# 另解：用 insert 逐一插入
words = ['Fly', 'robin', 'fly', 'Up', 'up', 'to', 'the', 'sky']
for k, x in enumerate(w * 2):
    words.insert(3 + k, x)
print(words)
