# -*- coding: utf-8 -*-
# Q：不用 Decimal 計算黃金比例至 30 位
# 知識點 id: q2_golden_int  |  參考解答 (非講義原文)

n = 30
SCALE = 10 ** (n + 5)            # 多保留 5 位當保護位數

a, b, count = 1, 1, 0
prev = None
while True:
    a, b = b, a + b              # 費氏數列
    count += 1
    ratio = b * SCALE // a       # 以整數運算取得放大後的比值
    digits = ratio // 10**5      # 截到小數點後 n 位
    if digits == prev:           # 連續兩次在第 n 位相同 → 收斂
        break
    prev = digits

s = str(digits)
print('count =', count, ' a =', a, ' b =', b)
print('黃金比例 ≈', s[0] + '.' + s[1:])
# 1.618033988749894848204586834365
