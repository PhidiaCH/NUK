# -*- coding: utf-8 -*-
# Example 3.3 range() 與 for
# 知識點 id: ex_range_for  |  講義程式

s, n = 0, 5
for i in range(n):
    s = s + i
    print(i, end='')
    if i < (n-1): print(end=' + ')
print(' = ', s)
print('sum(range(5)) = ', sum(range(5)))

notes = ['ti', 'do', 're', 'mi', 'fa', 'sol', 'la']
for i in range(len(notes)):
    print('notes[', i, '] : ', notes[i])

# 巢狀迴圈 (Nested Loop)
for i in range(10):
    for j in range(10):
        print((j+i) % 10, end='')
    print()
