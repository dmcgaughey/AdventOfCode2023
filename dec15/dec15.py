import numpy as np
import pandas as pd
import itertools

## Part 1     Find the weight of rock on a table
# with open('Dec15test.txt','r') as f:
with open('Dec15.txt','r') as f:
  lines = f.readlines()

line = lines[0]
hashList = []
hashvalue = 0
hashsum = 0
for c in line:
  if c ==',' or c=='\n':
    hashList.append(hashvalue)
    hashsum += hashvalue
    hashvalue = 0
    continue
  else:
    hashvalue = ((hashvalue + ord(c))*17)%256
# Need to process the last hashvalue since there is no ',' or endline
hashList.append(hashvalue)
hashsum += hashvalue

print(f'HashValue: {hashsum}')


## Main for Part 2