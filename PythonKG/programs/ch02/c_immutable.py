# -*- coding: utf-8 -*-
# 可變 vs 不可變 (mutable / immutable)
# 知識點 id: c_immutable  |  講義程式

text = 'Hello Python!'
try:
    text[5] = 's'
except TypeError as e:
    print('TypeError:', e)   # 'str' object does not support item assignment
print(text[:5] + 's' + text[6:])   # 改用切片產生新字串
