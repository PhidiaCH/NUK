# -*- coding: utf-8 -*-
# 5.1 set 集合 (可變)
# 知識點 id: c_set  |  講義程式

words = {'Hello', 'world', 'hello', 'Python', 'hello', 'sets'}
print(words)                 # 去除重複 + 不依次序
print('sets' in words)       # True  成員測試
print('Sets' in words)       # False
print(set('Python'))         # 字串拆成字元集合
print({'Python'})            # 只有一個元素的集合
print(type({}), type(set()))
