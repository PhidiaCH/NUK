# -*- coding: utf-8 -*-
# break / continue / pass / for-else
# 知識點 id: c_break  |  講義程式

for n in range(10):
    if n % 2 == 0:
        continue      # 跳過偶數
    if n > 7:
        break         # 離開迴圈
    print(n, end=' ') # 1 3 5 7
print()
for n in range(3):
    pass              # 佔位，不做事
else:
    print('loop finished without break')
