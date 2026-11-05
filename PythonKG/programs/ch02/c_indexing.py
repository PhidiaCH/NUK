# -*- coding: utf-8 -*-
# Indexing 索引
# 知識點 id: c_indexing  |  講義程式

text = 'Hello Python!'
print(text[0], text[3], text[12])   # H l !
print(text[-1], text[-7])           # ! P
print(repr(text[-8]))               # ' '
print(text[-0])                     # H
print(id(text[0]), id(text))        # id(): 物件的記憶體位址
# text[20]  # IndexError: string index out of range
