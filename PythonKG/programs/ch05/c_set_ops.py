# -*- coding: utf-8 -*-
# 集合運算 & | - ^
# 知識點 id: c_set_ops  |  講義程式

word_py1 = set('Python')
word_py2 = set('Pythagoras')
print(word_py2 & word_py1)   # {'P','h','o','t','y'}
print(word_py2 | word_py1)   # 聯集
print(word_py2 - word_py1)   # {'a','g','r','s'}
print(word_py1 - word_py2)   # {'n'}
print(word_py2 ^ word_py1)   # {'a','g','n','r','s'}
