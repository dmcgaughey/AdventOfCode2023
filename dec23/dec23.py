# import pandas as pd
import numpy as np
import sys
from enum import IntEnum
from heapq import heappop, heappush

POSITION = tuple[int, int]      #(x,y)

def one_step(pos,facing):
    return add_positons(pos, DIRECTION.delta1square(facing))

def add_positons(x:POSITION, delta:POSITION)->POSITION:
    new_pos = (x[0]+delta[0], x[1]+delta[1])
    return new_pos

def valid_position(x:POSITION,*,shape) -> bool:
    return x[0]>=0 and x[0]<=shape[0]-1 and x[1]>=0 and x[1]<=shape[1]-1

class ROTATE_DIR(IntEnum):
    CW =  1
    CCW = -1

# Define directions as an enum class
class DIRECTION(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3

    @staticmethod
    def rotate(dir:"DIRECTION", rot: ROTATE_DIR)->"DIRECTION":
        return DIRECTION((dir+rot+4)%4)

    @staticmethod
    def delta1square(dir:"DIRECTION")->POSITION:
        match dir:
            case DIRECTION.UP:
                out = (-1,0)
            case DIRECTION.RIGHT:
                out = (0,1)
            case DIRECTION.DOWN:
                out = (1,0)
            case DIRECTION.LEFT:
                out = (0, -1)
        return out

def backwards(dir: "DIRECTION") -> "DIRECTION":
    return DIRECTION((dir + 2 + 4) % 4)

def mdistance(start:POSITION, dest:POSITION) -> int:
    return abs(dest[0] - start[0]) + abs(dest[1] - start[1])

# Use a set for the searched datatype
def findPathDepthFirst(mymap,*,avoid_slopes=True)->int:
    branchesQ:list[tuple[POSITION, DIRECTION, int]] = []
    path = np.zeros(mymap.shape)
    blocked: set[tuple[POSITION, DIRECTION]] = set([])
    #searched = np.zeros(mymap.shape)

    max_path=0
    pos = (0, np.where(mymap[0,:]=='.')[0][0])
    facing = DIRECTION.DOWN
    branchesQ.append((pos,facing,1))
    while (branchesQ):
        pos, facing, path_len = branchesQ[-1]
        #print(pos)
        path[pos[0],pos[1]] = path_len
        # searched[pos[0],pos[1]] = path_len

        if pos[0]==mymap.shape[0]-1:    # At end?
            if path_len>max_path:
                max_path = path_len-1
            # Pop off branchesQ until last branch
            while (branchesQ):
                pos, facing, path_len = branchesQ.pop()
                if pos ==(-1,-1):
                    #branchesQ.pop()
                    break
                path[pos[0],pos[1]]=0
            continue

        # Find possible directions to walk
        new_dirs = 0
        # _facing = facing
        search_dirs = set([DIRECTION.RIGHT,DIRECTION.DOWN,DIRECTION.UP,DIRECTION.LEFT ]) - set([backwards(facing)])
        for _facing in search_dirs:              #range(4):
            # _facing = facing.rotate(_facing,ROTATE_DIR.CW)
            _pos = one_step(pos,_facing)
            terrain = mymap[_pos[0],_pos[1]]
            # or searched[_pos[0],_pos[1]]>path_len \
            # or (_pos, _facing) in blocked
            if terrain == '#' or path[_pos[0],_pos[1]]>0 \
                or avoid_slopes and \
                (
                (terrain=='>' and _facing==DIRECTION.LEFT) \
                or (terrain=='<' and _facing == DIRECTION.RIGHT) \
                or (terrain == 'v' and _facing == DIRECTION.UP) \
                or (terrain == '^' and _facing == DIRECTION.DOWN)
                ):\
                #or searched[_pos[0],_pos[1]] == -1:
                continue
            branchesQ.append((_pos,_facing,path_len+1))
            branchesQ.append(((-1,-1),-1,-1))
            new_dirs += 1
        if new_dirs==0:
            # Path is blocked or you are crossing path
            path[pos[0],pos[1]] = 0
            # pop off until previous branch
            while (branchesQ):
                pos, facing, path_len = branchesQ.pop()
                if pos ==(-1,-1):
                    # branchesQ.pop()
                    break
                path[pos[0],pos[1]]=0
                blocked.add((pos,facing))
                #searched[pos[0],pos[1]]=-1
            continue
        else:
            branchesQ.pop()     # Remove last branch indicator from


    return max_path

##################
## Main program
##
##
##
##
##################

with open('dec23test.txt', 'r') as f:
# with open('dec23.txt', 'r') as f:
    lines = f.readlines()
f.close()

mapList = []
for line in lines:
    mapList.append(list(line.strip()))

mymap = np.array(mapList)
print(mymap)

# cost = findPathDepthFirst(mymap)
# print(f'Bestpath: {cost}')

cost = findPathDepthFirst(mymap, avoid_slopes=False)
print(f'Bestpath: {cost}')

