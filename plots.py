#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, sys
#sys.path.insert(0, os.path.abspath(".."))

from file_manager import read_csv, create_csv
import numpy as np
import matplotlib.pyplot as plt
import math as m


if not os.path.exists("data.csv"):
    create_csv()
# {index:(time, initial grid, solution)}
data = read_csv()

# variables that will be used several time
totalTime = 0
averageTime = 0

#####################################################################
# average time according to number of filled in cells on beginning

times = [0] * 81
for i, j, k in data.values():
    times[81-j.count(".")] += float(i)

totalTime = sum(times)
averageTime = totalTime/len(times)
print("temps total :", totalTime)
# numbers of sudokus that starts with <index> clues
totalSudo = [0] * 81
for k, v in data.items():
    totalSudo[81-v[1].count('.')] += 1 

X = [i for i in range(81) if totalSudo[i]!=0]

avgTime = [i/j for i, j in zip(times, totalSudo) if j!=0]

plt.plot(X, avgTime)
plt.show()


#####################################################################
# maximum time according to number of filled in cells on beginning


maxTimes = [0] * 81
for i, j, k in data.values():
    curr = maxTimes[81-j.count(".")]
    if float(i) > curr:
        maxTimes[81-j.count(".")] = float(i)

X = [i for i in range(81) if maxTimes[i]!=0]
while 0 in maxTimes:
    maxTimes.remove(0)

plt.plot(X, maxTimes)
plt.show()


#####################################################################

# time, first three digits of solution

times = [[] for _ in range(81)]
for i, j, k in data.values():
    times[81-j.count(".")].append((k[:3], float(i)))

for n in range(len(times)):
    times[n] = list(filter(lambda x: float(x[1])>5, times[n]))

alltimes = []
for i in times:
    if len(i):
        alltimes += i
alltimes.sort()

# here we can see that, for the 17 clues grid, those that take more time have
# their first 3 digits very high (750+) but that's not the case for the other
# where the first 3 digits don't affect the time.
plt.scatter(*zip(*alltimes))
plt.show()


# To conclude, when the first 3 digits are higher, it affect the time of only
# a few of the grid. What is sure is that all grid with first 3 lower than 250
# have a low solving time.
# This is for solved sudoku but how to predict the time of an initial grid


######################################################################


# time, first three digits of initial grid
test17, test18 = [], []

DD = dict()
count = 99
for i, j, k in data.values():
    if 81-j.count(".") == 17:
        for n in j:
            if n != '.':
                test17.append((int(n), float(i)))
                break
    elif 81-j.count(".") == 18:
        for n in j:
            if n != '.':
                test18.append((int(n), float(i)))
                break

# the time is not affected by the first digit of the grid
plt.scatter(*zip(*test17))
plt.show()

# same here except for the few first
plt.scatter(*zip(*test18))
plt.show()

# no siginificant difference of time between low first digit
# and high first digit

#######################################################################

li3 = {17:set(), 18:set(), 21:set(), 22:set(), 23:set(), 24:set(), 25:set()}

s=0
for i, j, k in data.values():
    if 81-j.count(".") == 17:
        li3[17].add(float(i))
    elif 81-j.count(".") == 18:
        li3[18].add(float(i))
    elif 81-j.count(".") == 21:
        li3[21].add(float(i))
    elif 81-j.count(".") == 22:
        li3[22].add(float(i))
    elif 81-j.count(".") == 23:
        li3[23].add(float(i))
    elif 81-j.count(".") == 24:
        li3[24].add(float(i))
    elif 81-j.count(".") == 25:
        li3[25].add(float(i))
    s += float(i)


X = []
Y = []
# times for 17, 18, 21, 22, 23, 24 and 25 clues
for i, j in li3.items():
    for jj in j:
        X.append(i)
        Y.append(jj)
plt.scatter(X, Y, s=1)
plt.plot((16.5, 25.5), (120, 120))
plt.text(24.5, 150, s=">2min")
plt.plot((16.5, 25.5), (20, 20))
plt.show()
