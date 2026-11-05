# -*- coding: utf-8 -*-
# 4.1 基本序列運算 in / * / [] / +
# 知識點 id: c_seq_ops  |  講義程式

seq = []
for i in range(10):
    seq.append(i**2)
print(seq)            # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
print(seq[3])         # 9
print(seq[3:8])       # [9, 16, 25, 36, 49]
print(seq[3:8:3])     # [9, 36]
print([0] + seq[:3])  # 串接
print(seq * -1)       # [] 乘以負數得到空序列
