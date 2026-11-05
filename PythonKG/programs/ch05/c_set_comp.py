# -*- coding: utf-8 -*-
# Set Comprehension
# 知識點 id: c_set_comp  |  講義程式

word_py1 = set('Python')
word_py2 = set('Pythagoras')
print({x for x in word_py2 if x in word_py1})       # intersection
print({x for x in word_py2 if x not in word_py1})   # word_py2 - word_py1
print({x for x in word_py1 if x not in word_py2})   # word_py1 - word_py2
