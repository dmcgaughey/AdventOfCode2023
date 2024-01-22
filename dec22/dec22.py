# Dec 22: Falling Bricks
import numpy as np

def test_below(mymap,can_remove, brick):
	x, y, z = brick[0]
	xe, ye, ze = brick[1]
	dx, dy, dz = xe - x, ye - y, ze - z

	below = mymap[z-1, x:x+dx+1, y:y+dy+1]
	if below.shape == (1,1):
		below = below.squeeze(axis=1)
	else:
		below = below.squeeze()
	# ugh = below.shape
	# print('.',end='')

	if np.any(below == -1):	return
	below = set(below) - {0}
	if len(below) == 1:
		can_remove[below.pop()-1] = False

########################
# Part 1: Determine which brick are safe to remove without causing others to fall
########################
# with open('dec22test.txt', 'r') as f:
with open('dec22.txt', 'r') as f:
    lines = f.readlines()
f.close()

# Process each line to get the snapshot of each brick
bricks = []
for line in lines:
	start, end = line.split('~')
	start = tuple([int(s) for s in start.split(',')])
	end = tuple([int(e) for e in end.split(',')])
	bricks.append((start, end) )

bricks.sort(key = lambda x: x[0][2])

# Create a 3D map of the bricks
# mymap = np.zeros([10,3,3], dtype=int)
mymap = np.zeros([1000,10,10], dtype=int)
can_remove = np.ones([len(bricks)],dtype=bool)

mymap[0,:,:] = -1

for id, indx in enumerate(range(len(bricks)),1):
	start, end = bricks[indx]
	x, y, z = start
	xe, ye, ze = end
	dx, dy, dz = xe-x, ye-y, ze-z
	# Find the 2D slice that the brick occupies (1D for vertical brick)
	slice = mymap[:,x:x+dx+1,y:y+dy+1] # .squeeze()
	slice = slice.reshape([slice.shape[0],max(slice.shape[1:3])])
	# ned = slice.shape
	# print(f'{ned}')
	# Find the first row where all the entries are 0
	if dz == 0:
		zNew = np.max(np.where(np.any(slice!=0,axis=1))) + 1
	else:
		zNew = np.max(np.where(slice != 0)) + 1
	bricks[indx] = ((x,y,zNew),(xe,ye,zNew+dz))
	mymap[zNew:zNew+dz+1,x:x+dx+1,y:y+dy+1] = id

for brick in bricks:
	test_below(mymap,can_remove,brick)

safe_to_remove = np.sum(can_remove==True)
print(f'Part 1: Can remove without others falling: {safe_to_remove}')

########################
# Part 2: Determine how many bricks fall if a brick is removed
########################

def bricks_above(mymap:'numpy.ndarray', brick_indx)->tuple:
	return bricks_adjacent(mymap, brick_indx, +1)


def bricks_below(mymap: 'numpy.ndarray', brick_indx) -> tuple:
	return bricks_adjacent(mymap, brick_indx, -1)


def bricks_adjacent(mymap:'numpy.ndarray', brick_indx, offset)->set:
	start, end = bricks[brick_indx-1]
	x, y, z = start
	xe, ye, ze = end
	dx, dy, dz = xe - x, ye - y, ze - z

	if offset == +1:		# Searching above
		z_start = z+1 if dz == 0 else ze + 1
	elif offset == -1:		# Searching below
		z_start = z -1
	adjacent = mymap[z_start, x:x + dx + 1, y:y + dy + 1]
	if adjacent.shape == (1, 1):
		adjacent = adjacent.squeeze(axis=1)
	else:
		adjacent = adjacent.squeeze()
	adjacent = set(adjacent) -  {0}
	return adjacent


def test_fall(mymap, brick_indx,removed)-> bool:
	below = bricks_below(mymap, brick_indx)
	below = below - removed

	if -1 in below:    return False   # Can't fall from bottom
	return len(below) == 0



def count_falls(mymap, brick_indx:int, removed:set = set([]))->int:
	to_process_FIFO = [brick_indx]
	removed.clear()
	removed.add(brick_indx)

	num_falls = -1
	while to_process_FIFO:
		brick_indx = to_process_FIFO.pop()
		num_falls += 1

		above = bricks_above(mymap, brick_indx)
		if not above: continue

		above = tuple(above)
		for indx in range(len(above)):
			if (will_fall:=  test_fall(mymap,above[indx],removed)):
				if not above[indx] in removed:
					removed.add(above[indx])
					to_process_FIFO.insert(0,above[indx])

	return num_falls

total_falls = 0
for cnt in range(len(bricks)):
	if not can_remove[cnt]:
		total_falls += count_falls(mymap, cnt+1)

print(f'Part 2: Total bricks that fall as one is removed: {total_falls}')
print('Done')
