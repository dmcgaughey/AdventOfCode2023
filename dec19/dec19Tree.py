# import pandas as pd
import numpy as np
# import sys
from enum import IntEnum
# from heapq import heappop, heappush

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
    NONE = -1

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

def test_move(mymap, pos,facing,*,avoid_slopes=True)-> bool:
    if mymap[pos[0], pos[1]] == '#':
        return False
    if avoid_slopes:
        terrain = mymap[pos[0], pos[1]]
        if (terrain == '>' and facing == DIRECTION.LEFT) or (terrain == '<' and facing == DIRECTION.RIGHT) \
                or (terrain == 'v' and facing == DIRECTION.UP) or (terrain == '^' and facing == DIRECTION.DOWN):
            return False
    return True

def find_valid_search_dirs(mymap, pos,*,avoid_slopes=True)-> list[DIRECTION]:
    path_branches = []
    node_positions = []
    if test_move(mymap,[pos[0],pos[1]+1], DIRECTION.RIGHT, avoid_slopes=avoid_slopes):
        node_positions.append([pos[0],pos[1]+1])
        path_branches.append(DIRECTION.RIGHT)
    if test_move(mymap,[pos[0]+1,pos[1]], DIRECTION.DOWN, avoid_slopes=avoid_slopes):
        node_positions.append([pos[0]+1,pos[1]])
        path_branches.append(DIRECTION.DOWN)
    if test_move(mymap,[pos[0]-1,pos[1]], DIRECTION.UP, avoid_slopes=avoid_slopes):
        node_positions.append([pos[0]-1,pos[1]])
        path_branches.append(DIRECTION.UP)
    if test_move(mymap,[pos[0],pos[1]-1], DIRECTION.LEFT, avoid_slopes=avoid_slopes):
        node_positions.append([pos[0],pos[1]-1])
        path_branches.append(DIRECTION.LEFT)
    return path_branches, node_positions

def find_next_branch(mymap,pos:POSITION, facing:int,destination:POSITION,*,avoid_slopes=True)->list[POSITION,DIRECTION, int,POSITION]:
    length = 1
    node = [pos, facing, 0]

    if facing != DIRECTION.NONE:
        pos = one_step(pos, facing)

    while(1):
        if pos == destination:
            break               # exit while and return  (pos, facing, length)

        # search_dirs = set([DIRECTION.RIGHT, DIRECTION.DOWN, DIRECTION.UP, DIRECTION.LEFT]) - set([backwards(previous)])
        path_branches,_ = find_valid_search_dirs(mymap, pos,avoid_slopes=avoid_slopes)
        if backwards(facing) in path_branches: path_branches.remove(backwards(facing))

        if len(path_branches) ==1:  # range(4):
            # Move ahead
            facing = path_branches[0]
            pos = one_step(pos, facing)

            length += 1
        elif len(path_branches) >= 2:      # Have reached a branch node
            break
    node[2] = length
    init_pos, facing, length = node
    return init_pos,facing,length, pos

VERTICES = list[list[int, POSITION, POSITION, int, list]]
vertices:list[VERTICES] = []            # Vertices are node#, pos, end_pos, len, children

def find_node(vertices,pos, end_pos):
    for v in vertices:
        if v[1]==pos and v[2]==end_pos: return v
    return []

node_number = -1
def get_next_node_number():
    global node_number
    node_number += 1
    return node_number

# Use a set for the searched datatype
def findVerticeTree(mymap,pos, destination, facing = DIRECTION.DOWN, *,avoid_slopes=True)->int:
    # Find from the start of this branch to the next branch point
    pos, facing, length, next_pos = find_next_branch(mymap, pos, facing, destination, avoid_slopes=avoid_slopes)
    node = find_node(vertices,pos, next_pos)
    if not node:
        node = [get_next_node_number(), pos, next_pos, length, list([])]
        vertices.append(node)
    else:
        node[2] = next_pos
        node[3] = length

    # Check if you have reached the destination
    if next_pos == destination:
        new_node = find_node(vertices, next_pos, (-1,-1))
        if not new_node:
            new_node = [get_next_node_number(), next_pos, (-1,-1), 0, list([node[0]])]
            vertices.append(new_node)
        else:
            # Add the node to children of the new_node
            new_node[4].append(node[0])
            new_node[4] = list(set(new_node[4]))

        # Add the new_node to children of the node
        node[4].append(new_node[0])
        node[4] = list(set(node[4]))
        return length

    # Find all the branches from this node.
    path_facing, pos_start = find_valid_search_dirs(mymap, next_pos, avoid_slopes=avoid_slopes)

    for cnt in range(len(pos_start)):
        new_node = find_node(vertices, pos_start[cnt], (-1,-1))       #############   HERE ##############
        if not new_node:
            new_node = [get_next_node_number(), pos_start[cnt], (-1,-1), 0, list([node[0]])]
            vertices.append(new_node)
            # Update the children on the original node
            node[4].append(new_node[0])
            node[4] = list(set(node[4]))
            # Call the recursive function to find this node
            length += findVerticeTree(mymap, pos_start[cnt], destination, path_facing[cnt], avoid_slopes=avoid_slopes)
        else:   # New_node already existed no need to search again
            # Add the node to children of the new_node
            new_node[4].append(node[0])
            new_node[4] = list(set(new_node[4]))
            # Update the children on the original node
            node[4].append(new_node[0])
            node[4] = list(set(node[4]))
            # continue

    return length

def recurseDFS(start_node,end_node,path:list)->int:
    max_length = 0

    if start_node == end_node:
        return vertices[end_node][3]        # Return the pathlen for the last node (typically 0)

    if not path:
        path.append(vertices[start_node][1])
        # child = start_node[3][0]
        path.append(vertices[start_node][2])     # Push start and end for first node

    for child in vertices[start_node][4]:
        if vertices[child][2] in path:       # Check the positions on path -> positions can repeat in node #s
            continue        # This path backtracks
        path.append(vertices[child][2])      # Push the position onto the path
        length = vertices[start_node][3] + recurseDFS(child,end_node,path)
        if length > max_length: max_length=length
        path.pop()
    return max_length

def findLongestPath(vertices:VERTICES, start:POSITION, destination:POSITION)->int:
    path = list([])
    start_node = find_node(vertices, start)[0]
    end_node = find_node(vertices, destination)[0]
    length = recurseDFS(start_node,end_node,[])
    return length
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

start = pos = (0, np.where(mymap[0, :] == '.')[0][0])
destination = (mymap.shape[0]-1, np.where(mymap[-1, :] == '.')[0][0])
cost = findVerticeTree(mymap,start, destination, avoid_slopes=True)
longest = findLongestPath(vertices, start, destination)
print(f'Max path: {cost}')

# start = pos = (0, np.where(mymap[0, :] == '.')[0][0])
# destination = (-1, np.where(mymap[0, :] == '.')[0][0])
# cost = findVerticeTree(mymap, start, destination, avoid_slopes=False)
# print(f'Bestpath: {cost}')

