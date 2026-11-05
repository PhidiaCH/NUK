# -*- coding: utf-8 -*-
# Example 5.2 frozenset + list comprehension 字數統計
# 知識點 id: ex_frozen_wc  |  講義程式

words = ['Hello', 'world', 'hello', 'Python', 'list',
         'dictionary', 'tuple', 'hello', 'Hello',
         'set', 'tuple', 'python', 'dictionary', 'set',
         'array', 'binary', 'tuple', 'hello', 'data']
kw = frozenset(words)
word_counts = [(i, words.count(i)) for i in kw]
for w, c in word_counts:
    print('{0:15s} {1:2d}'.format(w, c))
