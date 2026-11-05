# -*- coding: utf-8 -*-
# 範例：搜尋質數 (解法二 for-else + break)
# 知識點 id: ex_prime2  |  講義程式

prime = []
for n in range(2, 100):
    for x in range(2, n):
        if n % x == 0:
            break
    else:
        # loop fell through without finding a factor
        prime.append(n)
        continue
    print('{:2d}'.format(n), end=' ')   # 合成數
print('\n are composite numbers less than 100.')
print('Prime Numbers (< 100) : ', prime)
