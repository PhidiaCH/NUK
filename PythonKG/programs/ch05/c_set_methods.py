# -*- coding: utf-8 -*-
# set 方法 add / remove / discard / pop / clear
# 知識點 id: c_set_methods  |  講義程式

words = set()
words.add(1);                 print(words)   # {1}
words = set([1, 2, 2, 3, 4, 5]); print(words) # {1, 2, 3, 4, 5}
words.remove(2);              print(words)
try:
    words.remove(2)
except KeyError as e:
    print('KeyError:', e)
words.discard(2)              # 不存在也不會出錯
print(words.pop())            # 任意一個元素
words.clear();                print(words)   # set()
