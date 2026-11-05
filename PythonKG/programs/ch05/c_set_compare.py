# -*- coding: utf-8 -*-
# 集合比較：子集合 / 超集合
# 知識點 id: c_set_compare  |  講義程式

set1 = {1, 2, 3, 4}
set2 = {1, 2, 3, 4, 5, 6}
print(set1 == set2, set1 != set2)   # False True
print(set1 > set2, set1 >= set2)    # False False
print(set1 < set2, set1 <= set2)    # True True
