import sympy as sp

POSITION = tuple[int, int, int]    # x,y or vx,vy
LINE3D = tuple[int, int, int, int, int, int]    # xo, yo, zo, vx, vy, vz

# There are 6 unknowns in intersection line (x0,y0,x0, vx,vy and vz) plus 1 more time for each point
# Thus 3 points gives 9 unkowns and 9 equations
def fit_line(lines:list[LINE3D])-> LINE3D:
  unknowns= sp.symbols('x0 y0 z0 vx vy vz t1 t2 t3')
  x0,y0,z0,vx,vy,vz,*time = unknowns

  # Not a linear equation so use symbolic solver.
  eqns = []
  for t, params in zip(time,lines[:3]):
    eqns.append(sp.Eq(params[0] + params[3]*t,  x0 + vx*t))
    eqns.append(sp.Eq(params[1] + params[4]*t,  y0 + vy*t))
    eqns.append(sp.Eq(params[2] + params[5]*t,  z0 + vz*t))

  result = sp.solve(eqns,unknowns)[0]
  return result[:6]


# ## Part 2     Find a line that intersects all the moving hailstones
# with open('dec24test.txt','r') as f:
with open('dec24.txt','r') as f:
  lines = f.readlines()

Line_List:list[LINE3D] = []
for line in lines:
  line = line.replace('@',',').strip()
  eqn =  [int(p) for p in line.split(',')]
  Line_List.append(eqn)

intercept_line = fit_line(Line_List)

print(f'Line through all ice: {intercept_line}')
print(f'Sum of initial coordinates: {sum(intercept_line[:3])}')