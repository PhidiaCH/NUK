# -*- coding: utf-8 -*-
# Example 5.1-7 以 set 做字數統計
# 知識點 id: ex_set_wc  |  講義程式

words = ['Hello', 'world', 'hello', 'Python', 'list',
         'dictionary', 'tuple', 'hello', 'Hello',
         'set', 'tuple', 'python', 'dictionary', 'set',
         'array', 'binary', 'tuple', 'hello', 'data']
key_words = set(words)
word_counts = []
for i in key_words:
    word_counts.append((i, words.count(i)))
for w, c in word_counts:
    print('{0:15s} {1:2d}'.format(w, c))
