# -*- coding: utf-8 -*-
"""Dec11.inpyb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PnsqHbSD462c-UlzeYz-yDA9CZvh9-nW

## Dec 11 2023:
"""

import numpy as np
import pandas as pd

#with open('Dec11Test.txt','r') as f:
with open('Dec11.txt','r') as f:
  lines = f.readlines()
map = []
for line in lines:
  map.append(list(line))

map = np.array(map, dtype=str)
map = np.delete(map,map.shape[1]-1,axis=1)
for col in range(map.shape[1]-1,-1,-1):
  if np.sum(map[:,col]=='#') == 0:
    newcol = np.zeros(map.shape[0],dtype=str)
    map = np.insert(map,col,newcol,axis=1)

for row in range(map.shape[0]-1,-1,-1):
  if np.sum(map[row,:]=='#') == 0:
    newrow = np.zeros(map.shape[1],dtype=str)
    map = np.insert(map,row,newrow,axis=0)

[galR, galC] = np.where(map=='#')
positions = []
for cnt in range(len(galR)):
  positions.append([galR[cnt], galC[cnt]])
positions = np.array(positions)

distance = 0
for cnt1 in range(len(positions)-1):
  for cnt2 in range(cnt1+1,len(positions)):
    distance += np.sum(np.abs(positions[cnt2,:]-positions[cnt1,:]))
distance

# Part 2
#Insert a million between each empty row or col
import numpy as np
import pandas as pd

with open('Dec11.txt','r') as f:
#with open('Dec11Test.txt','r') as f:
  lines = f.readlines()
map = []
for line in lines:
  map.append(list(line))

map = np.array(map, dtype=str)
map = np.delete(map,map.shape[1]-1,axis=1)

emptyRows =[]
emptyCols = []

for col in range(map.shape[1]-1,-1,-1):
  if np.sum(map[:,col]=='#') == 0:
    emptyCols.append(col)

for row in range(map.shape[0]-1,-1,-1):
  if np.sum(map[row,:]=='#') == 0:
    emptyRows.append(row)

emptyCols = np.sort(emptyCols)
emptyRows = np.sort(emptyRows)

[galR, galC] = np.where(map=='#')
positions = []
factor = 1000000
for cnt in range(len(galR)):
  tempR = factor * np.sum(emptyRows < galR[cnt]) + galR[cnt] - np.sum(emptyRows < galR[cnt])
  tempC = factor * np.sum(emptyCols < galC[cnt]) + galC[cnt] - np.sum(emptyCols < galC[cnt])
  positions.append([tempR,tempC])
positions = np.array(positions)

distance = 0
for cnt1 in range(len(positions)-1):
  for cnt2 in range(cnt1+1,len(positions)):
    distance += np.sum(np.abs(positions[cnt2,:]-positions[cnt1,:]))
distance

np.sum(emptyRows < galR[cnt])

positions

[galR, galC] = np.where(map=='#')
positions = []
for cnt in range(len(galR)):
  positions.append([galR[cnt], galC[cnt]])
positions = np.array(positions)

distance = 0
for cnt1 in range(len(positions)-1):
  for cnt2 in range(cnt1+1,len(positions)):
    distance += np.sum(np.abs(positions[cnt2,:]-positions[cnt1,:]))
distance

pal#Import the map
map = []
for line in lines:
  map.append(list(line.strip()))
map = np.array(map)

# Find the starting line
for lcnt in range(len(lines)):
  if not 'S' in lines[lcnt]: continue
  rowStart = lcnt
  break

for rcnt in range(len(lines[rowStart])):
  if lines[rowStart][rcnt]=='S':
    colStart = rcnt
    break

# Search all around the map for the two connecting values
path=[[rowStart,colStart]]
firstsquare = path[0]
nextsquare = search_node(map,path[0])
while(1):
  next = follow_node(map,nextsquare,firstsquare,path)
  if next:
    firstsquare = nextsquare
    nextsquare = next
  else:
    break

(len(path)-1)//2

map



path[:4]

path[-3:]

"""## Part 2"""

def map_adjacent_outside(map, outside, location):
  row = location[0]
  col = location[1]
  outside[row,col]= 1
  dirs = [[-1,0], [1,0], [0,-1], [0,1]]
  for step in dirs:
    if row+step[0]>=0 and row+step[0]<map.shape[0] and \
      col+step[1]>=0 and col+step[1]<map.shape[1]:
      if map[row+step[0],col+step[1]]=='.' and outside[row+step[0],col+step[1]] == 0:
        map_adjacent_outside(map,outside, [row+step[0],col+step[1]])

# Load small test file
#with open('Dec10testB.txt','r') as f:
with open('Dec10.txt','r') as f:
  lines = f.readlines()

#Import the map
map = []
for line in lines:
  map.append(list(line.strip()))
map = np.array(map)

#Replace the 'S' with the symbol determined above '|'
map[25,77] = '|'

# Check the array for any pipes that can be travelled between
# such as 7F or 7L and insert rows or columns with grounf between them

# Then find all adjecent to outside
# Then delete the added rows and columns
# Then count outside spaces
# Subtract the OUTSIDE from the total ground to get the enclosed

### 1  ADD col between pipes
map2 = np.copy(map)
operations = []
# Start by appending all '.' all around map2
#Append columns
newcol = np.zeros(map2.shape[0],dtype=str)
#print(newcol)
map2 = np.insert(map2,0,newcol,axis=1)
operations.append([0,1])
map2 = np.append(map2,np.expand_dims(newcol,axis=1),axis=1)
operations.append([map2.shape[1]-1,1])


# Append rows
newrow = np.zeros(map2.shape[1],dtype=str)
newrow.fill('.')
map2 = np.insert(map2,0,newrow,axis=0)
operations.append([0,0])
map2 = np.append(map2,np.expand_dims(newrow,axis=0),axis=0)
operations.append([map2.shape[0]-1,0])

for col in range(map2.shape[1]-1):
  temp = np.char.add(map2[:,col],map2[:,col+1])
  matches = np.isin(temp,['7F','7|','7L', '|F', '||', '|L', 'JF', 'J|','JL' ])
  if np.any(matches):
    #print(f'Append col {col}')
    #print(temp)
    map2 = np.insert(map2,col+1,map2[:,col+1],axis=1)
    map2[matches,col+1] = '.'
    operations.append([col+1, 1])

# Check each row for possible space between pipes and append rows as needed
for row in range(map2.shape[0]-1):
  temp = np.char.add(map2[row,:],map2[row+1,:])
  matches = np.isin(temp,['LF','L-','L7', '-F', '--', '-7', 'JF', 'J-','J7' ])
  if np.any(matches):
    #print(f'Append row {row}')
    #print(temp)
    map2 = np.insert(map2,row+1,map2[row+1,:],axis=0)
    map2[row+1,matches] = '.'
    operations.append([row+1, 0])


numGround = np.sum(map=='.')

# Find all the outside ground pieces
[Grows,Gcols] = np.where(map2=='.')

outside2 = np.zeros(map2.shape,dtype=int)
outside2[:,0] = 1
outside2[:,-1] = 1
outside2[0,:] = 1
outside2[-1,:] = 1

for iter in range(10):
  print(f'\n\nIter: {iter}')
  for cnt in range(len(Grows)):
    if (outside2[Grows[cnt],Gcols[cnt]]) == 0:
      #print (Grows[cnt],Gcols[cnt])
      #adjacent = outside2[Grows[cnt]-1,Gcols[cnt]] or \
      #  outside2[Grows[cnt]+1,Gcols[cnt]] or \
      #  outside2[Grows[cnt],Gcols[cnt]-1] or \
      #  outside2[Grows[cnt],Gcols[cnt]+1]
      adjacent = np.any(outside2[Grows[cnt]-1:Grows[cnt]+2,Gcols[cnt]-1:Gcols[cnt]+2])
      if adjacent:
        #print(outside2[Grows[cnt]-1:Grows[cnt]+2,Gcols[cnt]-1:Gcols[cnt]+2])
        print (Grows[cnt],Gcols[cnt])
        outside2[Grows[cnt],Gcols[cnt]] = 1
# Now undo all the operations to map2 and outside in the reverse order
map3 = np.copy(map2)
outside3 = np.copy(outside2)
opertionsCopy = operations.copy()
while (operations):
  op = operations.pop()
  map3 = np.delete(map3,op[0],axis=op[1])
  outside3 = np.delete(outside3,op[0],axis=op[1])

np.sum(map3=='.') -np.sum(outside3)

print(map3)

map.shape

140*140

np.sum(outside2)

np.sum(map2=='.')

outside2[:10,:10]

outside2[:10,-10:]

