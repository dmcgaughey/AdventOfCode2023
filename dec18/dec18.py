## Part 1    Digging Trench

import pandas as pd
import numpy as np
import sys
from enum import IntEnum
# sys.setrecursionlimit(20000)

class BTYPE(IntEnum):
    NOTDUG = 0
    DUG = 1
    INSIDE = 2
    OUTSIDE = 9

# def adjecent_outside(mymap,pos):
#     row = pos[0]
#     col = pos[1]
#
#     if mymap[row,col] != 0:
#         return
#     else:
#         mymap[row, col] = 2
#
#     for delta in ((1, 0), (-1, 0), (0, 1), (0, -1)):
#         if not (row + delta[0] < 0 or row + delta[0] > mymap.shape[0] - 1 \
#                 or col + delta[1] < 0 or col + delta[1] > mymap.shape[1] - 1):
#             if mymap[row + delta[0], col+delta[1]] == 0:
#                 adjecent_outside(mymap,[row + delta[0], col + delta[1]])
#     return
#
# def find_outside(mymap):
#     dotIndx = np.where(mymap == 0)
#     for cnt in range(len(dotIndx[0])):
#         row =  dotIndx[0][cnt]
#         col =  dotIndx[1][cnt]
#         if row==0 or row==mymap.shape[0]-1 or col==0 or col==mymap.shape[1]-1:
#             if mymap[row, col] == 0:
#                 adjecent_outside(mymap, (row, col))
#     return

def find_outside(mymap):
    mymap[mymap[:,0]==0,0] = BTYPE.OUTSIDE
    mymap[mymap[:,-1]==0,-1] = BTYPE.OUTSIDE
    mymap[0, mymap[0,:] == 0] = BTYPE.OUTSIDE
    mymap[-1,mymap[-1,:] == 0] = BTYPE.OUTSIDE

    iter = 0
    numNOTDUG = np.sum(mymap==BTYPE.NOTDUG)
    while (1):
        for col in range(1+iter,mymap.shape[1]):
            adjacent = np.logical_and(mymap[:,col-1]==BTYPE.OUTSIDE, mymap[:,col]==BTYPE.NOTDUG)
            mymap[adjacent,col] = BTYPE.OUTSIDE
            adjacent = np.logical_and(mymap[:, -col] == BTYPE.OUTSIDE, mymap[:, -col-1] == BTYPE.NOTDUG)
            mymap[adjacent, -col-1] = BTYPE.OUTSIDE

        for row in range(1+iter,mymap.shape[0]):
            adjacent = np.logical_and(mymap[row - 1,:] == 9, mymap[row,:] == BTYPE.NOTDUG)
            mymap[row,adjacent] = BTYPE.OUTSIDE
            adjacent = np.logical_and(mymap[-row ,:] == 9, mymap[-row-1,:] == BTYPE.NOTDUG)
            mymap[-row-1,adjacent] = BTYPE.OUTSIDE
        iter = iter+1
        if numNOTDUG == np.sum(mymap==BTYPE.NOTDUG):
            break
        else:
            numNOTDUG = np.sum(mymap == BTYPE.NOTDUG)

    return


# with open('dec18Test.txt', 'r') as f:
with open('dec18.txt','r') as f:
    lines = f.readlines()

ptList = [[0,0,'']]
for line in lines:
    code = line.split()

    match code[0]:
        case 'D':
            for _ in range(int(code[1])) :
                ptList.append([ptList[-1][0] + 1, ptList[-1][1], code[2] ])
        case 'U':
            for _ in range(int(code[1])):
                ptList.append([ptList[-1][0] - 1, ptList[-1][1], code[2]])
        case 'L':
            for _ in range(int(code[1])):
                ptList.append([ptList[-1][0] , ptList[-1][1] -1, code[2] ])
        case 'R':
            for _ in range(int(code[1])):
                ptList.append([ptList[-1][0], ptList[-1][1] + 1, code[2]])

ptDF = pd.DataFrame(ptList,columns=['r', 'c', 'color'])
ptDF.r = ptDF.r - ptDF['r'].min()
ptDF.c = ptDF.c - ptDF['c'].min()

mymap = np.zeros([ptDF['r'].max()+1, ptDF['c'].max()+1],dtype=int)
mymap[ptDF.r, ptDF.c] = BTYPE.DUG

# Now for each 0 (blank) need to see if it is encircled (count number of crossing between point an any edge (Choose a diagonal line to prevent problems with horizontal and vertical lines
ptDF.head(5)

find_outside(mymap)
mymap[mymap==BTYPE.NOTDUG] = BTYPE.INSIDE
area = np.sum(mymap==BTYPE.DUG) + np.sum(mymap==BTYPE.INSIDE)
print(f'Fill Area of {area}')