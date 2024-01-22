import numpy as np
import pandas as pd
import itertools

## Part 1     Find the weight of rock on a table
#with open('Dec14test.txt','r') as f:
with open('Dec14.txt','r') as f:
  lines = f.readlines()

inMatrix = []
# Need extra \n at end for this to process the last table
# Take care !!!!!!!!!
for line in lines:
  temp = line.strip().replace('O','1').replace('#','2').replace('.','0')
  inMatrix.append(list(temp))

Matrix = np.array(inMatrix,dtype = int)

for col in range(Matrix.shape[1]):
  squares = np.where(Matrix[:,col]==2)[0]

  if squares.size == 0:
    numRound = np.sum(Matrix[:,col] == 1)
    Matrix[:numRound,col] = 1
    Matrix[numRound:,col] = 0
  else:
    if (squares[-1] < Matrix.shape[0]-1):
      squares = np.append(squares,Matrix.shape[0])

    squares = squares[-1::-1]
    for sqcnt in range(len(squares)-1):
      sq1 = squares[sqcnt+1]
      sq2 = squares[sqcnt]
      numRound = np.sum(Matrix[sq1:sq2,col] == 1)
      Matrix[sq1+1:sq1+1+numRound,col] = 1
      Matrix[sq1+1+numRound:sq2,col] = 0
      #print(Matrix[:,col])

    # Now need to process between the last square rock and 0
    sq2 = squares[-1]
    if (sq2 >0):
      numRound = np.sum(Matrix[0:sq2,col] == 1)
      Matrix[0:numRound,col] = 1
      Matrix[numRound:sq2,col] = 0

mass = np.sum(np.sum(Matrix==1,axis=1) * np.arange(Matrix.shape[0],0,-1))

for r in range(Matrix.shape[0]):
  s = ''.join(str(Matrix[r,:]))
  print(s)

print(f'Mass: {mass}')
  # Find all the square rock # = 2


## Main for Part 2