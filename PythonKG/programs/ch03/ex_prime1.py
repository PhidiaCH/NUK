# -*- coding: utf-8 -*-
# 範例：搜尋小於 100 的質數 (解法一 in / not in)
# 知識點 id: ex_prime1  |  講義程式

prime_numbers = []
composite_numbers = []
for i in range(2, 11):
    for j in range(i*2, 100, i):
        composite_numbers.append(j)
for x in range(2, 100):
    if x not in composite_numbers:
        prime_numbers.append(x)
print('Prime Numbers (< 100) : ', prime_numbers)
