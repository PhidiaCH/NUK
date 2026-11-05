# -*- coding: utf-8 -*-
# 範例：樂透彩隨機選號
# 知識點 id: ex_lotto  |  講義程式
# 範例輸入: n

from random import random
min_num, max_num, six_num = 1, 49, 6

yorn = 'y'
while yorn == 'y' or yorn == 'Y':
    max_dim = max_num - min_num + 1
    lotto = []
    for i in range(max_dim):
        lotto.append(min_num + i)

    select = []
    for i in range(six_num):
        random_num = random() * 10000
        lotto_num = int(random_num % max_dim)
        select.append(lotto[lotto_num])
        for j in range(lotto_num, max_dim-1):
            lotto[j] = lotto[j+1]          # 移除已經選中的號碼
        max_dim -= 1

    print("\n 本期樂透彩 電腦選號 如下：(1 ~ 49)")
    for i in range(six_num):
        print(select[i], end='\t')
    yorn = input("\n 是否繼續 電腦選號？(y/n)：")
