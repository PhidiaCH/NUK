# -*- coding: utf-8 -*-
# Exercise 5.1 以 Set Comprehension 寫聯集與對稱差集
# 知識點 id: q5_1  |  參考解答 (非講義原文)

word_py1 = set('Python')
word_py2 = set('Pythagoras')

union = {x for s in (word_py1, word_py2) for x in s}
sym_diff = ({x for x in word_py1 if x not in word_py2} |
            {x for x in word_py2 if x not in word_py1})
# 或寫成單一 comprehension：
sym_diff2 = {x for x in word_py1 | word_py2
             if (x in word_py1) != (x in word_py2)}

print(union == word_py1 | word_py2, union)
print(sym_diff == word_py1 ^ word_py2, sym_diff)
print(sym_diff2 == sym_diff)
