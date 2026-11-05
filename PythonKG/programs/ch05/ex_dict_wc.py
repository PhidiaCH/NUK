# -*- coding: utf-8 -*-
# Example 5.3-7 以 dict 做字數統計
# 知識點 id: ex_dict_wc  |  講義程式

string = """Towers of gold are still too little
These hands could hold the world but it'll
Never be enough
Never be enough
For me"""
string1 = []
for line in string.splitlines():
    for w in line.split(sep=' '):
        string1.append(w)
key_words = set(string1)
d_counts = {}
for k in sorted(key_words):
    d_counts[k] = string1.count(k)
print(" << The sorted word-count result >>")
print("\t WORD \t\tCount \n ", "-"*32)
for k, v in d_counts.items():
    print('\t {0:15s} {1:2d}'.format(k, v))
