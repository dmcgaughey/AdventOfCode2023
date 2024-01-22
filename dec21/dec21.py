import numpy as np
import copy

POSITION = tuple[int, int]
def add_positons(x:POSITION, delta:POSITION)->POSITION:
    new_pos = (x[0]+delta[0], x[1]+delta[1])
    return new_pos

def valid_position(x:POSITION,shape) -> bool:
    return x[0]>=0 and x[0]<=shape[0]-1 and x[1]>=0 and x[1]<=shape[1]-1

# with open('dec21test.txt', 'r') as f:
with open('dec21.txt', 'r') as f:
    lines = f.readlines()
f.close()

mapList = []
for line in lines:
    mapList.append(list(line.strip()))

mymap = np.array(mapList)
print(mymap)

# Part 1: Brute force:  Find how many destination point in garden after N steps
start = np.where(mymap == 'S')
start =(start[0][0],start[1][0])

Nsteps = 1000
locations = set(tuple([]))
locations.add(start)
next_location = set()

_DELTA = ( (-1,0), (0,1), (1,0), (0,-1))
for _ in range(Nsteps):
    for pos in locations:
        for delta in _DELTA:
            new_pos = add_positons(pos,delta)
            if valid_position(new_pos,mymap.shape) and mymap[new_pos[0],new_pos[1]] != '#':
                next_location.add(new_pos)
    locations = copy.deepcopy(next_location)
    next_location.clear()

print(f'Part 1: {len(locations)} Steps {Nsteps}')

# Part 2: Infinite garden map: Too big to simulate
import sympy as sp

locations.clear()
locations.add(start)
next_location.clear()

Nsteps = [0, 65, 65+131, 65+262]
_DELTA = ( (-1,0), (0,1), (1,0), (0,-1))
length = []
locations.clear()
next_location.clear()
locations.add(start)

for cnt in range(1,len(Nsteps)):
    N = Nsteps[cnt]-Nsteps[cnt-1]
    print(Nsteps[cnt])
    for _ in range(N):
        for pos in locations:
            for delta in _DELTA:
                new_pos = add_positons(pos,delta)
                if mymap[new_pos[0]%mymap.shape[0], new_pos[1]%mymap.shape[1]] != '#':
                    next_location.add(new_pos)
        locations = copy.deepcopy(next_location)
        next_location.clear()
    length.append(len(locations))

# length =  [3848, 15407, 61185]
# Due to problem symmetry we can solve for eqn of x(n) = An**2+bn+c
eqns = []
unknowns = sp.symbols('A B C n')
A, B, C, n = unknowns

for cnt in range(3):
    eqns.append(sp.Eq(Nsteps[cnt+1]**2*A + Nsteps[cnt+1]*B + C,length[cnt]))

result = sp.solve(eqns,unknowns[:3])
print(result)

# A = 15186/17161
# B = 26976/17161
# C = 121238/17161

def f(n):
	f = result[A] * n**2 + result[B]*n + result[C]
	return f

N = 26501365
total = f(N)

print(f'Part 2: Total visited {total} in  {N} steps')