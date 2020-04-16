#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Sudoku solver, shortest version

import time as t

sudo1 = '019006000208310506060070010030601704187204053004800009401060030000100205090028460'
sudo2 = '001000000060000007300060890800009300030400200200805000000100004020040000000008526'
ijn = [(i, j, n) for i in range(9) for j in range(9) for n in range(1, 10)]

def back_track():
    for i in range(9):
        for j in range(9):
            if sdk[i][j]:
                continue
            for n in range(1, 10):
                if not produce_error(i, j, n):
                    sdk[i][j] = n
                    if back_track(): return True
                    sdk[i][j] = 0
            return False
    return True
    
def produce_error(r, c, n):
    if n in sdk[r] or n in [i[c] for i in sdk]: return True
    for j in range(3):
        if n in sdk[j+r-r%3][c-c%3:c-c%3+3]: return True
    
if __name__ == "__main__":
    t1 = t.time()
    for ss in (sudo1, sudo2, '0'*81):
        sdk = [list(map(int, ss[i:i+9])) for i in range(0, 81, 9)]
        if back_track():
            print(t.time() - t1)
            print("\n".join([" ".join(i) for i in [list(map(str, row)) for row in sdk]]))
        else:
            print("No solution exists")
