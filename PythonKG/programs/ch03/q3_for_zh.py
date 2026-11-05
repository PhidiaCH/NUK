# -*- coding: utf-8 -*-
# 練習：for 迴圈處理中文字串
# 知識點 id: q3_for_zh  |  參考解答 (非講義原文)

for i, ch in enumerate('第十個字母是六', start=1):
    print('第', i, '個字 :', ch)

names = ['齊天大聖', '孫悟空', '花果山水簾洞']
for name in names:
    print(name, '\t length =', len(name))
