# -*- coding: utf-8 -*-
# for 迴圈
# 知識點 id: c_for  |  講義程式

## (1) 輸出字串中的字母
i = 0
for alpha in 'Python 3.11.1':
    i = i + 1
    print(' 第 ', i, ' 個字母 :', alpha)

## (2) 輸出串列中的元素
languages = ['English', 'Python', 'Assembly']
for language in languages:
    print(' Language Version :', language)

## (3) 計算字串長度
for count in languages:
    print(count, '\t length =', len(count))
