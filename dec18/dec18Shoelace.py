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

def find_interior_points(Vertices):
    # Use shoelace thm to find area
    area = 0
    boundary = 0
    for cnt in range(len(Vertices)-1):
        area += 0.5 *(Vertices[cnt][0]*Vertices[cnt+1][1] - Vertices[cnt+1][0]*Vertices[cnt][1])
        boundary += abs(Vertices[cnt+1][0] - Vertices[cnt][0] + Vertices[cnt+1][1] - Vertices[cnt][1])
    # Use Pick's thm to find # points
    interior = area - boundary/2 + 1
    return interior + boundary


## Main Code
#############
# Part 1
#############
# with open('dec18Test.txt', 'r') as f:
with open('dec18.txt','r') as f:
    lines = f.readlines()
f.close()

Entry= tuple[int,int]
pos = [0,0]
Vertices:list[Entry] = [(pos)]

# Read all the lines and create the list of line segments
# Decode the hex value as the segment
for line in lines:
    code = line.split()
    match(code[0]):
        case 'R': dir = DIR.R
        case 'L': dir = DIR.L
        case 'U': dir = DIR.U
        case 'D': dir = DIR.D

    dist = int(code[1])

    # hex = code[2][2:7]     #.strip('#').strip('(').strip(')')[:-1]
    # dir = DIR(int(code[2][-2]))
    # dist = int('0x'+hex,16)

    match dir:
        case DIR.R:
            pos[0] = pos[0] + dist
            Vertices.append(tuple(pos))
        case DIR.L:
            pos[0] = pos[0] - dist
            Vertices.append(tuple(pos))
        case DIR.U:
            pos[1] = pos[1] - dist
            Vertices.append(tuple(pos))
        case DIR.D:
            pos[1] = pos[1] + dist
            Vertices.append(tuple(pos))

# Vertices = [(10,10), (10,11), (11,11),(11,10),(10,10)]
points = find_interior_points(Vertices)
print(f'Part 1: Number Points of {points}')

#############
# Part 2
#############
# with open('dec18Test.txt', 'r') as f:
# with open('dec18.txt','r') as f:
#     lines = f.readlines()

Entry= tuple[int,int]
pos = [0,0]
Vertices:list[Entry] = [(pos)]

# Read all the lines and create the list of line segments
# Decode the hex value as the segment
for line in lines:
    code = line.split()
    match(code[0]):
        case 'R': dir = DIR.R
        case 'L': dir = DIR.L
        case 'U': dir = DIR.U
        case 'D': dir = DIR.D

    # dist = int(code[1])

    hex = code[2][2:7]     #.strip('#').strip('(').strip(')')[:-1]
    dir = DIR(int(code[2][-2]))
    dist = int('0x'+hex,16)

    match dir:
        case DIR.R:
            pos[0] = pos[0] + dist
            Vertices.append(tuple(pos))
        case DIR.L:
            pos[0] = pos[0] - dist
            Vertices.append(tuple(pos))
        case DIR.U:
            pos[1] = pos[1] - dist
            Vertices.append(tuple(pos))
        case DIR.D:
            pos[1] = pos[1] + dist
            Vertices.append(tuple(pos))

# Vertices = [(10,10), (10,11), (11,11),(11,10),(10,10)]
points = find_interior_points(Vertices)
print(f'Part2: Number Points of {points}')