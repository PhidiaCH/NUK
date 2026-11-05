# -*- coding: utf-8 -*-
# list 方法
# 知識點 id: c_list_methods  |  講義程式

words = ['Fly', 'robin', 'fly', 'Up', 'up', 'to', 'the', 'sky']
print(words.index('up'))       # 4
print(words.count('fly'))      # 1
w = []
w.extend(words[0:3])           # ['Fly', 'robin', 'fly']
words.insert(3, w); print(words)
words.remove(w);    print(words)
words.insert(3, 'Fly')
del words[3]
words.sort();       print(words)  # 大寫字母排在小寫之前
print(words.pop())             # 'up'
print(words.pop(3))            # 'robin'
print(words)

a = ['A', 'b', 'C']
b = a.copy(); c = a.copy()
b.append([1.41, 3.14])         # 加入「一個」元素 (巢狀串列)
c.extend([1.41, 3.14])         # 逐一加入元素
print(b, c)
