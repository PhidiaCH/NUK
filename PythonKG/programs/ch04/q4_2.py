# -*- coding: utf-8 -*-
# Exercise 4.2 用 list 實作 Queue 佇列 (FIFO)
# 知識點 id: q4_2  |  參考解答 (非講義原文)
# 範例輸入: a / b / c / null

def Queue(prompt=' Enqueue (type null if done): '):
    queue = []
    while True:
        item = input(prompt)
        if item in ('n', 'nu', 'nul', 'null'):
            break
        queue.append(item)                     # enqueue
    print('\n Within Queue: ', queue)
    print(' >>> Dequeue --> FIFO : First-In-First-Out ')
    while queue:                               # 非空串列為 True
        print(' dequeue : ', queue.pop(0))     # dequeue
    print(' ******* Queue = ', queue)

Queue()
