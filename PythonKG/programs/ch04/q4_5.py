# -*- coding: utf-8 -*-
# Exercise 4.5 字數統計 Word Counts (Never Enough)
# 知識點 id: q4_5  |  參考解答 (非講義原文)

lyrics = """I'm trying to hold my breath
Let it stay this way
Can't let this moment end
You set off a dream with me
Getting louder now
Can you hear it echoing?
Take my hand
Will you share this with me?
'Cause darling without you
All the shine of a thousand spotlights
All the stars we steal from the nightsky
Will never be enough
Never be enough
Towers of gold are still too little
These hands could hold the world but it'll
Never be enough
Never be enough
For me
Never, never
Never, never
Never, for me
Never enough
Never enough
Never enough
For me
For me
For me
For me"""

# (1) 一般寫法
words = []
for w in lyrics.split():
    words.append(w.rstrip('?,.!'))
counts = []
for k in sorted(set(words)):
    counts.append((k, words.count(k)))
for k, c in counts:
    print('{0:12s}{1:3d}'.format(k, c))

# (2) List Comprehension 精簡版
words = [w.rstrip('?,.!') for w in lyrics.split()]
print('\n'.join('{0:12s}{1:3d}'.format(k, words.count(k)) for k in sorted(set(words))))
