import numpy as np
import pandas as pd
from enum import IntEnum

# Dec 10 Traverse a path
class Symbols(IntEnum):
  F = 0
  S7 = 1
  J = 2
  L = 3
  UD = 4
  RL = 5
  NONE=-1

def convert_symbol(text:str)->Symbols:
  match text:
    case 'F': sym = Symbols['F']
    case 'J': sym = Symbols['J']
    case '7': sym = Symbols['S7']
    case 'L': sym = Symbols['L']
    case '|': sym = Symbols['UD']
    case '-': sym = Symbols['RL']
    case _: sym = Symbols['NONE']
  return sym

class Direction(IntEnum):
  N = -1
  U = 0
  R = 1
  D = 2
  L = 3

POSITION = tuple[int, int]    # x,y

def add_positions(p1:POSITION, p2:POSITION)-> POSITION:
  return p1[0]+p2[0], p1[1]+p2[1]

# Look up table for symbols F,7,J,L,|, -
_NEXT_DIR = np.array( [ [Direction.R,  Direction.L, Direction.N, Direction.N, Direction.U, Direction.N ],  # Facing UP
                        [Direction.N,  Direction.D, Direction.U, Direction.N, Direction.N, Direction.R ],  # Facing R
                        [Direction.N,  Direction.N, Direction.L, Direction.R, Direction.D, Direction.N ],  # Facing D
                        [Direction.D,  Direction.N, Direction.N, Direction.U, Direction.N, Direction.L ]  # Facing L
                      ], dtype=Direction)

_DELTA = ( (-1,0), (0,1), (1,0), (0,-1))
def next_square(pos:POSITION, facing:Direction,symbol:Symbols)->tuple[Direction,POSITION]:
  next_dir = _NEXT_DIR[facing,symbol]
  return next_dir, add_positions(pos,_DELTA[next_dir])

def find_start_symbol(mymap,start:POSITION)->Direction:
  dirs = [Direction.N, Direction.N]
  dcnt = 0

  right = add_positions(start,(0,1))
  if mymap[right[0],right[1]] in'-7J':
    dirs[dcnt] = Direction.R
    dcnt +=1

  left = add_positions(start, (0, -1))
  if mymap[left[0], left[1]] in '-FL':
    dirs[dcnt] = Direction.L
    dcnt += 1

  up = add_positions(start, (-1, 0))
  if mymap[up[0], up[1]] in '|7F':
    dirs[dcnt] = Direction.U
    dcnt += 1

  down = add_positions(start, (1, 0))
  if mymap[down[0], down[1]] in '|LJ':
    dirs[dcnt] = Direction.D
    dcnt += 1

  match (dirs[0], dirs[1]):
    case (Direction.R, Direction.L): sym = '-'
    case (Direction.R, Direction.U): sym = 'L'
    case (Direction.R, Direction.D): sym = '7'
    case (Direction.L, Direction.U): sym = 'J'
    case (Direction.L, Direction.D): sym = 'F'
    case (Direction.U, Direction.D): sym = '|'

  mymap[start[0],start[1]] = sym
  facing = dirs[0]

  return facing


def find_loop(mymap,start:POSITION)->int:
  vertices: list[POSITION]  = []

  facing = find_start_symbol(mymap,start)
  pos = start
  perimeter = 0
  while not(vertices and pos == start):
    perimeter += 1
    if mymap[pos[0],pos[1]] != '|' and mymap[pos[0],pos[1]] != '-':
      vertices.append(pos)
    facing, pos = next_square(pos,facing, convert_symbol(mymap[pos[0],pos[1]]))
  return perimeter, vertices


def find_enclosed_points(Vertices,boundary):
  # Use shoelace thm to find area
  area = 0
  # boundary = 0
  for cnt in range(len(Vertices) - 1):
    area += 0.5 * (Vertices[cnt][0] * Vertices[cnt + 1][1] - Vertices[cnt + 1][0] * Vertices[cnt][1])
    # boundary += abs(Vertices[cnt + 1][0] - Vertices[cnt][0] + Vertices[cnt + 1][1] - Vertices[cnt][1])
  # Use Pick's thm to find # points
  interior = abs(area) - boundary / 2 + 1
  return interior


# with open('Dec10test.txt','r') as f:
with open('Dec10.txt','r') as f:
  lines = f.readlines()

#Import the map
mymap = []
for line in lines:
  mymap.append(list(line.strip()))
mymap = np.array(mymap)

# Find the starting line
start = np.where(mymap=='S')
start = (start[0][0], start[1][0])
# Search all around the map for the two connecting values
perimeter, vertices = find_loop(mymap,start)

vertices.append(vertices[0])
num_pts = find_enclosed_points(vertices,perimeter)

print(f'Perimeter: {perimeter}')
print(f'Num Pts: {num_pts}')