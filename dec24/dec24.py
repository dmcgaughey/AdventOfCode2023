import numpy as np
import pandas as pd
import itertools
import math

POSITION = tuple[int, int]    # x,y or vx,vy
LINE = tuple[float, float]    # y = mx+b

def line_from_time_eqns(x_t:LINE, y_t:LINE)->LINE:
  # Given x=vx*t_x0 and y =vy*t+y0  Find y = mx+b
  # Soln: m = vy/vx and b= y0-vy/vx*x0
  return (y_t[0]/x_t[0], y_t[1] - y_t[0]/x_t[0]*x_t[1])

def intersection (line0:LINE, line1:LINE)->POSITION:
  # Given y=mx+b where line0: m=line0[0] and b=line0[1] (same for line 1)
  # Find Intersection of line0 and line1
  # Soln: x_i = (b1-b0)/(m1-m0) and then use this in either eqn for yi (y_i = m_0*x_i+b_0)

  # check for parallel lines
  if line0[0] == line1[0]:
    x_i, y_i = math.inf, math.inf
  else:
    x_i = (line1[1]-line0[1])/(line0[0]-line1[0])
    y_i = line0[0]*x_i + line0[1]
  return(x_i,y_i)

def invert_eqn(line: LINE, soln):
  # Given a line x=m*t + x0 and a position (soln), invert the eqn and find the independent variable (t)
  if line[0] != 0:
    return (soln-line[1])/line[0]
  else:
    return math.inf

Line_List:list[tuple[LINE,LINE,LINE]] = []

# ## Part 1     Find the weight of rock on a table
# with open('dec24test.txt','r') as f:
with open('dec24.txt','r') as f:
  lines = f.readlines()

LINE_LIST:list[LINE] = []
for line in lines:
  pos_, vel_ = line.split('@')

  pos = [ int(p) for p in pos_.split(',')]
  vel = [ int(v) for v in vel_.split(',')]

  x_t_eqn = LINE([vel[0],pos[0]])
  y_t_eqn = LINE([vel[1],pos[1]])
  y_x_eqn = line_from_time_eqns(x_t_eqn,y_t_eqn)
  Line_List.append([x_t_eqn,y_t_eqn,y_x_eqn])

# Now check all pairs of lines for intersection
# BOTTOM_LEFT = LINE((7,7))
# TOP_RIGHT = LINE((27,27))
BOTTOM_LEFT = LINE((200000000000000,200000000000000))
TOP_RIGHT = LINE((400000000000000,400000000000000))


num_intersections = 0
for cnt0 in range(len(Line_List)-1):
  for cnt1 in range(cnt0+1,len(Line_List)):
    x_i,y_i = intersection(Line_List[cnt0][2],Line_List[cnt1][2])
    if x_i>=BOTTOM_LEFT[0] and x_i<=TOP_RIGHT[0] \
      and y_i>=BOTTOM_LEFT[1] and y_i<=TOP_RIGHT[1]:
      # Check that the intersection occurs at positive time
      if not (invert_eqn(Line_List[cnt0][0],x_i)<0 or invert_eqn(Line_List[cnt0][1],y_i)<0 \
          or invert_eqn(Line_List[cnt1][0],x_i)<0 or invert_eqn(Line_List[cnt1][1],y_i)<0) :
        num_intersections += 1

print(f'Intersection: {num_intersections}')