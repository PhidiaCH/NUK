# -*- coding: utf-8 -*-
# 參照 (alias) vs 複製 (copy)
# 知識點 id: c_alias  |  講義程式

listNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
list0 = listNumbers           # alias: 同一個物件
list0.append('a')
print(listNumbers)            # 也多了 'a' !

listNumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 0]
list1 = []
list1.extend(listNumbers)     # Method 1 : extend()
list2 = listNumbers.copy()    # Method 2 : copy()
list3 = listNumbers[:]        # Method 3 : slicing
list1.append('A'); list2.append(2020); list3.append(None)
print(listNumbers)            # 不變
print(list0 is listNumbers, list2 is listNumbers)
