#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Sudoku opener, Python 3.5.2

import csv

#sample
#[[1, 7, 0, 3, 2, 0, 0, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 5, 1],
# [0, 0, 0, 0, 8, 0, 0, 0, 0],
# [5, 0, 6, 0, 0, 1, 0, 0, 0],
# [0, 0, 0, 7, 0, 0, 3, 0, 0],
# [4, 0, 0, 0, 0, 0, 0, 0, 0],
# [0, 0, 0, 5, 0, 4, 0, 6, 0],
# [0, 8, 0, 0, 0, 0, 2, 0, 0],
# [0, 0, 0, 0, 0, 0, 0, 0, 0]]

# a sudoku is a list of 9 lists of 9 elements
# sudokuList is a list of all sudokus
sudokuList = []

def database_to_list():
    """Take the sudokus in the database and reshape them to lists of lists"""
    with open('sudo_DB.txt', 'r') as DB:
        for line in DB:
            sudoTmp = []
            for i in range(9):
                sudoTmp.append(line[9*i:9*i+9])
            for ind, l in enumerate(sudoTmp):
                l = l.replace('.', '0')
                l = [int(c) for c in l if c != '\n']
                sudoTmp[ind] = l
            sudokuList.append(sudoTmp)
    return sudokuList

def list_to_database(sudo):
    """Take the sudoku solved and bring it back to a string"""
    sudoku = ""
    if isinstance(sudo[0], int): # 81 ints
        sudoku = "".join(map(str, sudo))
    elif isinstance(sudo[0], list): # 9x9 matrix
        for row in sudo:
            sudoku += "".join([str(i) for i in row])
    with open('DB_solutions.txt', 'a') as DBs:
        DBs.write(sudoku + "\n")

def get_data():
    """Take the data we want for the csv"""
    listOfSudo, listOfSol, listOfTimes = [], [], []
    with open("sudo_DB.txt", 'r') as sudo:
        for line in sudo:
            listOfSudo.append(line[:-1])
    with open("DB_solutions.txt", 'r') as solutions:
        for line in solutions:
            listOfSol.append(line[:-1])
    with open("times.txt", 'r') as times:
        for time in times:
            time = time.split(" ")
            # the last part is the time in sec
            listOfTimes.append(time[-1][:-1])
    return listOfSudo, listOfSol, listOfTimes

def create_csv():
    """Put the data in a csv"""
    sudo, sol, times = get_data()
    with open("data.csv", 'w') as file:
        writer = csv.writer(file, delimiter=';', quoting=csv.QUOTE_ALL)
        data = zip(range(1, len(sudo)+1), times, sudo, sol)
        writer.writerow(['number', 'time', 'initial', 'solution'])
        for index, time, sudo, sol in data:
            writer.writerow([index, time, sudo, sol])

def read_csv():
    """Get the data in the csv in a dictionnary"""
    dataDict = {} # {index:(time, initial grid, solution)}
    indexes, times, inits, sols = [], [], [], []
    with open("data.csv", 'r') as file:
        reader = csv.reader(file, delimiter=';')
        Tindex, Ttime, Tinit, Tsol = next(reader)
        for row in reader:
            # -1 because the first row was the column titles
            dataDict[int(row[0]) - 1] = (row[1], row[2], row[3])
    return dataDict
        
        
