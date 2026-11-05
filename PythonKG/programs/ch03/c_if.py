# -*- coding: utf-8 -*-
# if / elif / else
# 知識點 id: c_if  |  講義程式
# 範例輸入: 0.5

x = float(input("Please enter a number: "))
if x < 0:
    print(x, 'is less than zero !')
elif x == 0:
    print('0')
elif x == 1:
    print('1')
else:
    print(x, ' > 0')
