# -*- coding: utf-8 -*-
# Exercise 5.3 以 comprehension 精簡 dict 字數統計
# 知識點 id: q5_3  |  參考解答 (非講義原文)

string = """Towers of gold are still too little
These hands could hold the world but it'll
Never be enough
Never be enough
For me"""
words = [w for line in string.splitlines() for w in line.split(' ')]
d_counts = {k: words.count(k) for k in sorted(set(words))}
print('\n'.join('\t {0:15s} {1:2d}'.format(k, v) for k, v in d_counts.items()))
