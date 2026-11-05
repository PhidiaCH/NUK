# -*- coding: utf-8 -*-
# Example 4.1 seq * n 的共用參照陷阱
# 知識點 id: ex_repeat_alias  |  講義程式

list1 = [[1]]
list2 = list1 * 2
list2[0].append(2)
print(list2)            # [[1, 2], [1, 2]]  兩個元素是同一個物件!

list1 = []
for i in range(4):
    list1.append([])    # 4 個不同的空串列
list2 = [[]] * 4        # 4 個參照指向同一個空串列

def list_elements(list0):
    for i in range(len(list0)):
        list0[i].append(2*i)
    return list0

print('list1 (after) = ', list_elements(list1))  # [[0], [2], [4], [6]]
print('list2 (after) = ', list_elements(list2))  # [[0, 2, 4, 6]] * 4
