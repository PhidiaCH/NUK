# -*- coding: utf-8 -*-
# Exercise 5.5 字數統計 Revisited (10 行內)
# 知識點 id: q5_5  |  參考解答 (非講義原文)

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
words = [w.rstrip('?,.!') for w in lyrics.split()]               # list
counts = {k: words.count(k) for k in sorted(set(words))}         # set + dict
width = max(len(k) for k in counts)
print('\n'.join(f'{k:<{width}} {v:>2}' for k, v in counts.items()))  # tuple
