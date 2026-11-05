# -*- coding: utf-8 -*-
# 練習：插入位置與 or 條件
# 知識點 id: q3_insert  |  參考解答 (非講義原文)

fruits = ['apple', 'mango', 'watermelon', 'banana', 'pineapple']
pos = fruits.index('pineapple')        # banana 與 pineapple 之間
for f in fruits[:]:
    if len(f) <= 6 or len(f) > 9:
        fruits.insert(pos, f)
        pos += 1                       # 保持原插入順序
print(fruits)
