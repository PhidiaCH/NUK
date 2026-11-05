# -*- coding: utf-8 -*-
# Example 4.2-4 用 list 實作 Stack 堆疊 (LIFO)
# 知識點 id: ex_stack  |  講義程式
# 範例輸入: a / b / c / d / null

def Stack(prompt=' Push to Stack (type null if done): '):
    stack = []
    while True:
        top = input(prompt)
        if top in ('n', 'nu', 'nul', 'null'):
            break
        else:
            stack.append(top)               # push

    print('\n Within Stack: ', stack)
    print(' <<< Pop the Stack --> LIFO : Last-In-First-Out ')
    for _ in range(len(stack)):
        print(' pop Stack : ', stack.pop())  # pop
    print(' ******* Stack = ', stack)

Stack()
