#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Database checker, Python 3.5.2

import file_manager as fm
import Sudoku_solver as ss
import time as t
from pprint import pprint


DATABASE = fm.database_to_list()

def counter(sudoku):
    """count the number of filled cells"""
    count = 0
    for i in sudoku:
        for j in i:
            if j != 0:
                count += 1
    return count

def counter_dup(dico):
    """
    Count the cells that have two possibilities to see if guess
    loop is actually useful
    """
    # only few of the sudokus don't have any double poss in their dict
    c = 0
    for i, j in dico.items():
        if len(j) == 2:
            c += 1
    return c

def count_filled(grid):
    """Return the number of filled cells in the sudoku"""
    c = 0
    for line in grid:
        c += line.count(0)
    return 81 - c

# make a function that look how many filled cells there are
# if 17 or 18, try the guess loop, otherwise the logic loop
# should be enough. See plots for the max time 

def test2(dico):
    return sum([len(v) for v in dico.values()])

def solve_DB():
    """Run the sudoku for the entire database and write solutions"""
    global sudo
    for ind, sudoku in enumerate(DATABASE):
        t0 = t.time()
        ss.initialize(sudoku)
        ss.logic_loop()
        ss.guess_loop()
        if ss.modif:
            ss.logic_loop()
        #solver.shuffle_poss()
        ss.order_COORD_LIST()
        # less than 1s to get there
        sudo = ss.back_track(ss.sudoku)
        try:
            if ss.complete(sudo):
                t1 = t.time()
                print(ind, 'completed in', t1 - t0)
                fm.list_to_database(sudo)
                with open('times.txt', 'a') as tm:
                    tm.write("{} completed in {}\n".format(ind, t1-t0))
            else:
                print("No solution exists")
                ss.display()
        except TypeError:
            print("No solution exists")
