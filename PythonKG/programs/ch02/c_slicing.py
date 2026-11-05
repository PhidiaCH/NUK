# -*- coding: utf-8 -*-
# Slicing 切片
# 知識點 id: c_slicing  |  講義程式

text = 'Hello Python!'
print(text[:5])        # 'Hello'
print(text[3:])        # 'lo Python!'
print(text[3:20])      # 'lo Python!'
print(repr(text[20:])) # ''  empty string
print(text[-1:1:-1])   # '!nohtyP oll'
print(text[:6] + 'world!')        # 'Hello world!'
print(text[6:10] + 'agoras')      # 'Pythagoras'
