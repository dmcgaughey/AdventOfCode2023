## Part 1    Digging Trench

import pandas as pd
import numpy as np
import sys
from enum import IntEnum
# sys.setrecursionlimit(20000)

class DIR(IntEnum):
    N = -1
    R = 0
    D = 1
    L = 2
    U = 3

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

def isenclosed(pos,lineList)->bool:
    crossings = 0
    # Check a line from current point edge going UP
    for segment in lineList:
        # On Segment
        if (segment['dir'] == DIR.U or segment['dir'] == DIR.D) and pos[0]==segment['offset']:    # moving UD and segment is on same X as position
            if pos[1]>= segment['start'] and pos[1]<= segment['end']:
                return True
            elif pos[1] > segment['end']:
                crossings += int(segment['cross'])

        if (segment['dir'] == DIR.R or segment['dir'] == DIR.L) and pos[0]> segment['start'] and pos[0]< segment['end']:      # Segment moved LR and is on same Y
            if pos[1]==segment['offset']:
                return True                     # on the line
            elif pos[1]>segment['offset']:
                crossings += 1                  # Below line

    return bool(crossings%2)

        # Check if crossing segment


# def find_area(lineList):
#     for line in lineList:
#         step = 1 if line[2]> line[1] else -1
#         match line[0]:
#             case DIR.RL:
#                 # Test above
#                 y = line[3]
#                 for x in (line[2],line[3],step):
#                     if isenclosed((x,y),lineList)):
#
#                 # Test Below
#             case DiR_UD:
#                 # Test Right
#                 # Test Left
#
#     # Find min and max in (x,y)
#     minx = min(lineList, key = lambda x: x[1] if x[0]==DIR.RL else x[3]+1)[1]
#     maxx = max(lineList, key = lambda x: x[2] if x[0]==DIR.RL else x[3]-1)[2]
#     miny = min(lineList, key=lambda x: x[1] if x[0] == DIR.UD else x[3]+1)[1]
#     maxy = max(lineList, key=lambda x: x[2] if x[0] == DIR.UD else x[3]-1)[2]
#     # For each point test if it is enclosed
#     area = 0
#     for cntx in range(minx,maxx+1):
#         for cnty in range(miny,maxy):
#             if isenclosed((cntx,cnty),lineList): area+=1
#     return area

def find_area(lineList):
    # Find min and max in (x,y)
    minx = min(lineList, key = lambda x: x['start'] if (x['dir']==DIR.R or x['dir']==DIR.L) else x['offset']+1)['start']
    maxx = max(lineList, key = lambda x: x['end'] if (x['dir']==DIR.R or x['dir']==DIR.L) else x['offset']-1)['end']
    miny = min(lineList, key = lambda x: x['start'] if (x['dir']==DIR.U or x['dir']==DIR.D) else x['offset']+1)['start']
    maxy = max(lineList, key=lambda x: x['end'] if (x['dir'] == DIR.U or x['dir'] == DIR.D) else x['offset'] - 1)['end']

    # For each point test if it is enclosed
    # testmap = np.zeros([maxy-miny+1,maxx-minx+1])
    area = 0
    for y in range(miny,maxy+1):
        for x in range(minx,maxx+1):
            if isenclosed((x,y),lineList):
                area+=1
                # testmap[y,x] += 1
    return area


## Main Code
with open('dec18Test.txt', 'r') as f:
# with open('dec18.txt','r') as f:
    lines = f.readlines()

Entry= dict['dir':DIR, 'cross':bool, 'start':int, 'stop':int, 'offset':int]       # (direction=UD or RL, start, end, offset (x0 or y0)
lineList:list[Entry] = []

pos = [0,0]

# Read all the lines and create the list of line segments
# Decode the hex value as the segment
for line in lines:
    code = line.split()

    hex = code[2][2:7]     #.strip('#').strip('(').strip(')')[:-1]
    dir = DIR(int(code[2][-2]))
    dist = int('0x'+hex,16)

    match dir:
        case DIR.R:
            lineList.append({'dir':dir,'cross':False,'start':pos[0],'end':pos[0] + dist, 'offset':pos[1]})
            pos[0] = pos[0]+dist
        case DIR.L:
            lineList.append( {'dir':DIR.L, 'cross':False,'start': pos[0] - dist, 'end':pos[0], 'offset':pos[1]} )
            pos[0] = pos[0] - dist
        case DIR.U:
            lineList.append({'dir': DIR.U, 'cross':False,'start': pos[1] - dist, 'end':pos[1], 'offset':pos[0]})
            pos[1] = pos[1] - dist
        case DIR.D:
            lineList.append({'dir': DIR.D, 'cross':False,'start': pos[1], 'end':pos[1] + dist, 'offset':pos[0]})
            pos[1] = pos[1] + dist

# Now need to fill in the next line values
for cnt in range(1,len(lines)-1):
    lineList[cnt]['cross'] =  lineList[cnt-1]['dir'] == lineList[cnt+1]['dir']
# Special cases for first and last line in list
lineList[0]['cross'] = lineList[-1]['dir'] == lineList[1]['dir']
lineList[-1]['cross'] = lineList[-2]['dir'] == lineList[0]['dir']

area = find_area(lineList)
print(f'Fill Area of {area}')