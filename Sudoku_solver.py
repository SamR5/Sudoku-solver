#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Sudoku solver, Python 3.5.2

import time as t
import itertools as it
import random as r
import file_manager as fm


sudoku1 =\
[[0, 0, 0, 0, 0, 0, 4, 1, 0],
 [9, 0, 0, 3, 0, 0, 0, 0, 0],
 [3, 0, 0, 0, 2, 0, 0, 0, 0],
 [0, 4, 8, 0, 0, 7, 0, 0, 0],
 [0, 0, 0, 0, 0, 0, 0, 5, 2],
 [0, 1, 0, 0, 0, 0, 0, 0, 0],
 [5, 0, 0, 2, 0, 0, 0, 0, 6],
 [0, 7, 0, 0, 0, 0, 8, 0, 0],
 [0, 0, 0, 0, 9, 0, 0, 0, 0]]

sudoku2 =\
[[0, 0, 1, 0, 0, 0, 0, 0, 0],
 [0, 6, 0, 0, 0, 0, 0, 0, 7],
 [3, 0, 0, 0, 6, 0, 8, 9, 0],
 [8, 0, 0, 0, 0, 9, 3, 0, 0],
 [0, 3, 0, 4, 0, 0, 2, 0, 0],
 [2, 0, 0, 8, 0, 5, 0, 0, 0],
 [0, 0, 0, 1, 0, 0, 0, 0, 4],
 [0, 2, 0, 0, 4, 0, 0, 0, 0],
 [0, 0, 0, 0, 0, 8, 5, 2, 6]]

grid =\
[[1, 0, 0, 0, 4, 8, 0, 0, 0],
 [0, 5, 0, 0, 0, 0, 9, 0, 0],
 [0, 0, 6, 7, 0, 0, 3, 0, 0],
 [0, 0, 0, 5, 7, 0, 2, 0, 0],
 [8, 0, 3, 4, 0, 0, 0, 0, 0],
 [0, 0, 0, 9, 8, 0, 0, 0, 0],
 [0, 0, 0, 3, 0, 0, 0, 4, 1],
 [6, 7, 0, 8, 0, 0, 0, 0, 0],
 [0, 0, 0, 2, 0, 0, 0, 0, 0]]

ss3 = [4, 0, 0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 8, 0, 0, 0, 0, 0,
       0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 5, 0, 0, 9, 0, 0, 8, 0, 0, 0, 0,
       6, 0, 0, 0, 7, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 2, 7, 0, 0,
       5, 0, 3, 0, 0, 0, 0, 4, 0, 9, 0, 7, 0, 0, 0, 0, 0, 0]
sdk = []
for i in range(9):
    sdk.append(ss3[i*9:i*9+9])
ss3 = sdk
empty = [[0 for _ in range(9)] for _ in range(9)]


# cells coordinates : (line, column)
# from (0, 0) to (8, 8)
# +-----------------------+
# | block | block | block |
# | (0,0) | (0,1) | (0,2) |
# |-------+-------+-------|
# | block | block | block |
# | (1,0) | (1,1) | (1,2) |
# |-------+-------+-------|
# | block | block | block |
# | (2,0) | (2,1) | (2,2) |
# +-----------------------+

# the list of all coordinates of the sudoku
COORD_LIST = tuple(i for i in it.product(range(9), repeat=2))
# {(block):(coordinates of each cell)}
BLOCKS = {}
for row in range(3):
    for col in range(3):
        BLOCKS[(row, col)] = tuple()
        for i in range(3):
            for j in range(3):
                BLOCKS[(row, col)] += ((i + 3*row, j + 3*col),)

# double for generators
# created once because used many times (avoids lots of creations)
FORFOR3 = tuple(it.product(range(3), range(3)))

#In [6]: %timeit for i in range(9): pass
#437 ns ± 0.566 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
#In [7]: %timeit for i in (0, 1, 2, 3, 4, 5, 6, 7, 8): pass
#165 ns ± 0.0938 ns per loop (mean ± std. dev. of 7 runs, 10000000 loops each)

# used to treat a 1D list (len=81) as if it was a 9*9 list of list
blocks3 = ((0, 1, 2, 9, 10, 11, 18, 19, 20),
           (3, 4, 5, 12, 13, 14, 21, 22, 23),
           (6, 7, 8, 15, 16, 17, 24, 25, 26),
           (27, 28, 29, 36, 37, 38, 45, 46, 47),
           (30, 31, 32, 39, 40, 41, 48, 49, 50),
           (33, 34, 35, 42, 43, 44, 51, 52, 53),
           (54, 55, 56, 63, 64, 65, 72, 73, 74),
           (57, 58, 59, 66, 67, 68, 75, 76, 77),
           (60, 61, 62, 69, 70, 71, 78, 79, 80))
def dd(n):
    s = []
    n = n%9
    for i in range(9):
        s.append(n+9*i)
    return tuple(s)
LINES = {i:tuple(range(i//9*9, i//9*9+9)) for i in range(81)}
COLS = {i:dd(i) for i in range(81)}
BLOCKS2 = {i:blocks3[j] for j in range(9)
                        for i in range(81) if i in blocks3[j]}
# cells adjacent for flattened sudoku
LCB2 = {i:set(LINES[i] + COLS[i] + BLOCKS2[i]) for i in range(81)}
# cells adjacent for nested sudoku ## useless
LCB = {(i//9, i%9):set((j//9, j%9)) for i in range(81) for j in LCB2[i]}

def initialize(sudo):
    """Initalize the parameters for the sudoku (list of lists)"""
    global possDict, modif, sudoku
    sudoku = sudo
    # {(coord):set 1 to 9} all possibilities at initial state
    possDict = {(i, j):{*range(1, 10)} for i, j in COORD_LIST}
    modif = False # flag if function changed possDict
    
def display(sudoku):
    """Display the grid"""
    try:
        sudoku[0][0]
    except:
        sdk = []
        for i in range(9):
            sdk.append(sudoku[i*9:i*9+9])
        sudoku = sdk
    print('+' + '-' * 23 + '+')
    rowind = 0
    for row in [[*map(str, row)] for row in sudoku]:
        row.insert(3, '|'); row.insert(-3, '|')
        print('|', " ".join(row), '|')
        if rowind in (2, 5):
            # line separating blocks horizontally
            print('|' + ('-' * 7 + '+') * 2 + '-' * 7 + '|')
        rowind += 1
    print('+' + '-' * 23 + '+')
    
def look_poss():
    """Filtrate the possDict with potential solutions of each cell"""
    global possDict
    for k, v in possDict.items():
        if len(v) < 2: # no need to search for them
            continue
        possDict[k] -= impossible_sol(k)
    
def isolated_poss():
    """Replace the cell if only one value is in the possibilities"""
    global sudoku, modif
    for coord, val in possDict.items():
        if len(val) == 1:
            sudoku[coord[0]][coord[1]] = val.pop()
            modif = True
    
def impossible_sol(coord):
    """Return a set of values that can't be in the cell coord"""
    coo1, coo2 = coord
    # if the cell is already filled
    if sudoku[coo1][coo2]:
        return {1, 2, 3, 4, 5, 6, 7, 8, 9}
    # find the block containing the number to check
    # since blocks sides are three, block coord = cell coord // 3
    block = BLOCKS[(coo1 // 3, coo2 // 3)]
    # set of all possibilities
    imp = set()
    # add all numbers != 0 in the row
    for i in sudoku[coo1]:
        if i:
            imp.add(i)
    # add all numbers != 0 in the column
    for i in sudoku:
        if i[coo2]:
            imp.add(i[coo2])
    # add all numbers != 0 in the block
    for i, j in block:
        if sudoku[i][j]:
            imp.add(sudoku[i][j])
    return imp
    
def unique_sol_block():
    """
    1. Search for unique solution in the block
    2. Search for solution only in one line (or col) in block
    """
    global sudoku, modif, possDict
    # check block by block
    for cells in BLOCKS.values():
        # list possibilities of each cell
        blockposs = [p for cell in cells for p in possDict[cell]]
        #blockposs = []
        #for cell in cells:
        #    # put all solution of each cells in
        #    blockposs += [p for p in possDict[cell]]
        # if a number is repeted only one time in the
        # possibilities of the block, then it is the 
        # solution for the cell that contains it
        for i in blockposs:
            if blockposs.count(i) == 1:
                # find the cell with the solution
                for cc in cells:
                    if i in possDict[cc]:
                        # then replace with the number
                        sudoku[cc[0]][cc[1]] = i
                        modif = True
                        break
        # If a poss appears only in the same line of a block, the poss
        # is eliminated from the rest of the line (same for columns)
        for i in blockposs:
            if blockposs.count(i) == 2:
                # find the cell with the solution
                dup = [cell for cell in cells if i in possDict[cell]]
                # because the second pass, they will be deleted
                if len(dup) != 2:
                    continue
                # if they have the same row
                if dup[0][0] == dup[1][0]:
                    for k in possDict.keys():
                        # for each cell in the same row
                        if k[0] == dup[0][0] and k not in dup:
                            possDict[k] -= {i}
                # if they have the same column
                elif dup[0][1] == dup[1][1]:
                    for k in possDict.keys():
                        # for each cell in the same column
                        if k[1] == dup[0][1] and k not in dup:
                            possDict[k] -= {i}
            if blockposs.count(i) == 3:
                # find the cell with the solution
                dup = [cell for cell in cells if i in possDict[cell]]
                # because the second pass, they will be deleted
                if len(dup) != 3:
                    continue
                # if they have the same row
                if dup[0][0] == dup[1][0] == dup[2][0]:
                    for k in possDict.keys():
                        # for each cell in the same row
                        if k[0] == dup[0][0] and k not in dup:
                            possDict[k] -= {i}
                # if they have the same column
                elif dup[0][1] == dup[1][1] == dup[2][1]:
                    for k in possDict.keys():
                        # for each cell in the same column
                        if k[1] == dup[0][1] and k not in dup:
                            possDict[k] -= {i}
    
def unique_sol_line():
    """Search for unique solution in the line"""
    global sudoku, modif
    # check line by line
    for ind1, line in enumerate(sudoku):
        lineposs = [] #list possibilities of each cell
        for ind2, cell in enumerate(line):
            # put all solution of each cells in
            lineposs += [p for p in possDict[(ind1, ind2)]]
        # if a number is repeted only one time in the
        # possibilities of the line, then it is the 
        # solution for the cell that contains it
        for i in lineposs:
            if lineposs.count(i) == 1:
                # find the cell with the solution
                for ind3, cell in enumerate(line):
                    if i in possDict[(ind1, ind3)]:
                        # then replace with the number
                        sudoku[ind1][ind3] = i
                        modif = True
                        break
    
def unique_sol_column():
    """Search for unique solution in the column"""
    global sudoku, modif
    rotSudoku = zip(*sudoku[::-1])
    # check line by line of the rotated sudoku
    for ind1, line in enumerate(rotSudoku):
        lineposs = [] #list possibilities of each cell
        for ind2, cell in enumerate(line):
            # coord are reverse because the grid is rotated
            # put all solution of each cells in
            lineposs += [p for p in possDict[(ind2, ind1)]]
        # if a number is repeted only one time in the
        # possibilities of the line, then it is the 
        # solution for the cell that contains it
        for i in lineposs:
            if lineposs.count(i) == 1:
                # find the cell with the solution
                for ind3, cell in enumerate(line):
                    # coord are reverse because the grid is rotated
                    if i in possDict[(ind3, ind1)]:
                        # then replace with the number
                        sudoku[ind3][ind1] = i
                        modif = True
                        break
    
def naked_pairs_triples():
    """Filtrate possibles if multiples are present in the row/col"""
    global possDict
    # for rows
    for row in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        # list of all poss of the line
        vals = [possDict[(row, c)] for c in range(9) if len(possDict[(row, c)])]
        for poss in vals:
            # if 2 pairs or 3 triples or ...
            if vals.count(poss) == len(poss):
                for c in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    # delete poss if not itself
                    if possDict[(row, c)] != poss:
                        possDict[(row, c)] -= poss
    # for columns
    for col in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        # list of all poss of the column
        vals = [possDict[(r, col)] for r in range(9) if len(possDict[(r, col)])]
        for poss in vals:
            # if 2 pairs or 3 triples or ...
            if vals.count(poss) == len(poss):
                for R in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    # delete poss if not itself
                    if possDict[(R, col)] != poss:
                        possDict[(R, col)] -= poss
    
def xwing():
    """X-wing technique"""
    global possDict
    # find all combinations of 2 rows and 2 columns
    for rows in it.combinations((0, 1, 2, 3, 4, 5, 6, 7, 8), 2):
        for cols in it.combinations((0, 1, 2, 3, 4, 5, 6, 7, 8), 2):
            # if a cell is filled noting to do
            if sudoku[rows[0]][cols[0]] or\
               sudoku[rows[0]][cols[1]] or\
               sudoku[rows[1]][cols[0]] or\
               sudoku[rows[1]][cols[1]]:
                continue
            # list of all poss of the X-wing
            pp = tuple(possDict[(rows[0], cols[0])] &
                       possDict[(rows[0], cols[1])] &
                       possDict[(rows[1], cols[0])] &
                       possDict[(rows[1], cols[1])])
            
            if not len(pp):
                continue
            break2 = False
            # filtrate columns
            for i in pp:
                # for each column != cols #{cols[0], cols[1]}
                for c in {0, 1, 2, 3, 4, 5, 6, 7, 8} - {*cols}:
                    # if i is in a column
                    if i in possDict[(rows[0], c)] or\
                       i in possDict[(rows[1], c)]:
                        break2 = True
                        break
                if break2:
                    break
                # now i is not in both lines so cols are filtated
                for R in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    if R not in rows:
                        possDict[(R, cols[0])] -= {i}
                        possDict[(R, cols[1])] -= {i}
            break2 = False
            # filtrate lines
            for i in pp:
                # for each row != rows
                for R in {0, 1, 2, 3, 4, 5, 6, 7, 8} - {*rows}:
                    # if i is in a line
                    if i in possDict[(R, cols[0])] or\
                       i in possDict[(R, cols[1])]:
                        break2 = True
                        break
                if break2:
                    break
                # now i is not in both lines so cols are filtated
                for c in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                    if c not in cols:
                        possDict[(rows[0], c)] -= {i}
                        possDict[(rows[1], c)] -= {i}
    
def logic_loop(fromGuess=False):
    """Find obvious and unique solutions"""
    global modif
    modif = False
    
    isolated_poss() # fills the cells with one possibility
    look_poss() # update possDict
    #check unique solutions and update grid
    unique_sol_block() # check each block
    unique_sol_line() # check each line
    unique_sol_column() # check each column
    look_poss() # update possDict
    isolated_poss() # look for cells with one possibility
    look_poss() # update possDict
    naked_pairs_triples() # look for naked pairs, triples, ...
    xwing() # rarly useful (x8 slower than other)
    # if it generates isolated, they will be changes after next loop
    # because possDict should have changed
    # as long as the possibilities changes, all operations are repeted
    if modif and not fromGuess:
            return logic_loop()
    isolated_poss() # ensure that no 1-poss pass to the back track

def guess_loop():
    """
    Try a cell from the possDict, go through the logic_loop,
    if after that there errors, it's definitly not the answer
    """
    global sudoku, possDict, modif
    modif = False
    # in case logic_loop found all
    oldPossDict = {k:v.copy() for k, v in possDict.items()}
    for coord, poss in oldPossDict.items():
        # isolated_poss at end of logic_loop prevent one-poss
        if not poss: # if empty
            continue
        oldGrid = [l[:] for l in sudoku]
        oldPossDict = {k:v.copy() for k, v in possDict.items()}
        # errors are generated when poss > 2 even if we just remove
        # the poss that created the error off the dict
        poss = tuple(poss)
        sudoku[coord[0]][coord[1]] = poss[0]
        possDict[coord].clear()
        logic_loop(fromGuess=True)
        # if the replacement produced an error
        # in both cases the dict and grid return to their old
        # state. Abscence of errors != warranty of solution
        if errors(sudoku):
            sudoku = oldGrid
            possDict = oldPossDict
            if len(poss) == 2:
                modif = True
                # if one generated errors, it's the other
                sudoku[coord[0]][coord[1]] = poss[-1]
                possDict[coord].clear()
            else:
                modif = True
                # if more than 2poss, removed from possDict
                possDict[coord] -= {poss[0]}
        else:
            sudoku = oldGrid
            possDict = oldPossDict
    if oldPossDict != possDict:
        return guess_loop()

def order_COORD_LIST():
    """
    Order the COORD_LIST from fewest possibilities to the maximum
    of possibilities. A 2-poss cell has a probability of 0.5 to fail
    and if it fails, half of that tree of all poss is dismissed.
    A 6-poss cell has a probability of 0.83 to fail, and 20% of
    the tree is dismissed
    """
    global COORD, possDict, sudoku
    # here lines are kept in order
    # and 0-poss aren't appended
    COORD = []
    for R in (0, 1, 2, 3, 4, 5, 6, 7, 8):
        for p in (1, 2, 3, 4, 5, 6, 7, 8, 9):
            for c in (0, 1, 2, 3, 4, 5, 6, 7, 8):
                if len(possDict[(R, c)]) == p:
                    COORD.append(R*9+c)
    COORD = tuple(COORD)
    # flatten the possDict and sudoku
    sudoku = [item for sublist in sudoku for item in sublist]
    possDict = {9*a+b:possDict[(a, b)] for a, b in possDict.keys()}
    
def shuffle_poss():
    """Shuffle the possibilities in the possDict"""
    global possDict
    for k, v in possDict.items():
        v = list(v)
        r.shuffle(v)
        possDict[(k)] = v

def back_track(ss):
    """Back-track"""
    for i in COORD:
        if not ss[i]: # if the cell is 0, check each possibilities
            # poss of cell (i, j) = poss - (line + column + block)
            for n in sorted(possDict[i] - set(ss[j] for j in LCB2[i])):
                ss[i] = n
                if back_track(ss):
                    return ss
                ss[i] = 0
            return False
    return ss # if all cells are 0

def errors(sudoku):
    """
    Return True if there are errors in the grid (otherwise False)
    """
    # in case the sudoku is flattened
    try:
        sudoku[0][0]
    except:
        sdk = []
        for i in range(9):
            sdk.append(sudoku[i*9:i*9+9])
        sudoku = sdk
    # errors in rows
    for row in sudoku:
        for i in row:
            # if a number (!=0) appears more than once
            if not i: # if i == 0: no check
                continue
            if row.count(i) > 1:
                return True
    # errors in columns
    grid2 = zip(*sudoku[::-1])
    for row in grid2:
        for i in row:
            # if a number (!=0) appears more than once
            if not i: # if i == 0: no check
                continue
            if row.count(i) > 1:
                return True
    # errors in blocks
    for cells in BLOCKS.values():
        # add all values of the block if they are != 0
        valOfBlock = [(sudoku[i][j]) for i, j in cells\
                                     if sudoku[i][j]] # != 0
        #if there is twice or more the same value, there is an error
        if len(valOfBlock) != len(set(valOfBlock)):
            return True
    return False

def complete(sudoku):
    """Return True if all cells are filled"""
    if errors(sudoku):
        return False
    if isinstance(sudoku[0], int):
        if 0 in sudoku:
            return False
    else:
        for i, j in it.product(range(9), range(9)):
            if not sudoku[i][j]: # if == 0:
                return False
    return True

if __name__ == "__main__":
    # lighten the possDict
    DATABASE = fm.database_to_list()
    for sudoku in DATABASE:#(sudoku1, sudoku2):#, ss3):#, grid):
        t0 = t.time()
        initialize(sudoku)
        logic_loop()
        guess_loop()
        if modif:# > 5:
            logic_loop()
        order_COORD_LIST()
        sudoku = back_track(sudoku)
        print(t.time() - t0)
        if not complete(sudoku):
            display(sudoku)
    #display()
