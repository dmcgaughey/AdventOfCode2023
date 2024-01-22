# import pandas as pd
import numpy as np
import sys
from enum import IntEnum
from heapq import heappop, heappush

POSITION = tuple[int, int]      #(x,y)

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

def mdistance(start:POSITION, dest:POSITION) -> int:
    return abs(dest[0] - start[0]) + abs(dest[1] - start[1])

# Use a set for the searched datatype
searchNode = tuple[POSITION, DIRECTION, int]
heapNode = tuple[int, POSITION, DIRECTION, int]         # cost, position, direction, numblocks
searched = set()
def findPathDyksra(mymap,*,minblocks=1,maxblocks=10):
    global searched
    destination = (mymap.shape[0] -1, mymap.shape[1]-1)    # add_positons(mymap.shape,(-1,-1))      #

    # Clear the searched set (may be running multiple times)
    searched = set()  # set[searchNode]

    heap: list[heapNode] = [(0, (0, 0), DIRECTION.DOWN,1), (0,(0,0), DIRECTION.RIGHT,1)]
    # heappush(heap,(0, (0, 0), DIRECTION.DOWN,1))
    # heappush(heap,(0,(0,0), DIRECTION.RIGHT,1))

    while (heap):
        cost, pos, dir, numblocks = heappop(heap)

        if (pos,dir,numblocks) in searched:
            continue                    # Already here with a lower or equal score
        searched.add((pos,dir,numblocks))

        if pos == destination and numblocks>=minblocks:
            return cost

        if pos != (0,0) and numblocks>=minblocks:
            # Turn CCW
            test_dir = DIRECTION.rotate(dir,ROTATE_DIR.CCW)
            test_pos = add_positons(pos, DIRECTION.delta1square(test_dir))
            if valid_position(test_pos,shape=mymap.shape):
                heappush(heap,(cost+mymap[test_pos[0],test_pos[1]], test_pos, test_dir,1))

            # Turn CW
            test_dir = DIRECTION.rotate(dir, ROTATE_DIR.CW)
            test_pos = add_positons(pos, DIRECTION.delta1square(test_dir))
            if valid_position(test_pos,shape=mymap.shape):
                heappush(heap, (cost + mymap[test_pos[0], test_pos[1]], test_pos, test_dir, 1))

        # Continue straight
        if numblocks < maxblocks:
            test_pos = add_positons(pos, DIRECTION.delta1square(dir))
            if valid_position(test_pos, shape=mymap.shape):
                heappush(heap, (cost + mymap[test_pos[0], test_pos[1]], test_pos, dir, numblocks+1))
    return -1

##################
## Main program
##
##
##
##
##################

# with open('dec17Test.txt', 'r') as f:
with open('dec17.txt', 'r') as f:
    lines = f.readlines()
f.close()

mapList = []
for line in lines:
    mapList.append(list(line.strip()))

mymap = np.array(mapList, dtype=int)
print(mymap)

cost = findPathDyksra(mymap,minblocks=0,maxblocks=3)
print(f'Bestpath: {cost}')

cost = findPathDyksra(mymap,minblocks=4,maxblocks=10)
print(f'Bestpath: {cost}')