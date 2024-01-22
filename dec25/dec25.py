import random
import numpy as np

nameList = []
def get_name_indx(name):
	global nameList
	if name not in nameList:
		name_indx = len(nameList)
		nameList.append(name)
	else:
		name_indx = nameList.index(name)
	return name_indx

def find_path(nodes:list[list],src:int, target:int)->list:
	path = []
	loc = src
	while loc != target:
		randomList =  random.sample(nodes[loc][1],len(nodes[loc][1]))
		for possible in randomList:
			if possible!=loc and possible not in path:
				loc = possible
				path.append(loc)
				break
		else:
			return []	# No path found: looped around on self somehow
	return path

def count_nodes(node_indx)->int:
	count = 0
	visited = [False]*len(nodes)
	to_visitQ = [node_indx]
	while to_visitQ:
		node_indx = to_visitQ.pop()
		visited[node_indx] = True
		for child in nodes[node_indx][1]:
			if not visited[child] and child not in to_visitQ:
				to_visitQ.insert(0,child)
	return(sum(visited))

########################
# Part 1: Find 3 cut to divide into two dets
########################
# with open('dec25test.txt', 'r') as f:
with open('dec25.txt', 'r') as f:
	lines = f.readlines()
f.close()

nodes = []
for line in lines:
	name, destinations = line.strip().split(':')

	name_indx = get_name_indx(name)
	destinations = [get_name_indx(d) for d in destinations.split()]

	node = [name_indx, destinations]
	nodes.append(node)

nodes.sort(key = lambda x: x[0])

# Add in nodes not on input line so can use array indexing
for cnt in range(len(nameList)):
	if cnt>len(nodes)-1 or nodes[cnt][0]!=cnt:
		nodes.insert(cnt,[cnt,[]])

for parent in nodes:
	for child in parent[1]:
		if parent[0] not in nodes[child][1]:
			nodes[child][1].append(parent[0])

#############
# Part 1: Stochastic Approach
#############
edge_counts = {}
for cnt in range(10000):
	#if cnt%100: print(cnt)
	src, dest = random.sample( [x for x in range(0,len(nodes))], 2)
	path = find_path(nodes,src,dest)

	for cnt in range(len(path)-1):
		edge = tuple(sorted([path[cnt], path[cnt+1]]))
		edge_counts[edge] = edge_counts.get(edge,0) + 1

most_visited = sorted(edge_counts.items(),key=lambda x: x[1], reverse=True)
for edge in most_visited[:3]:
	print(f'Cut {nameList[edge[0][0]]} to {nameList[edge[0][1]]}')

# Count group sizes
# Cut egdes the you found
for edge, count in most_visited[:3]:
	nodes[edge[0]][1].remove(edge[1])
	nodes[edge[1]][1].remove(edge[0])
count1 = count_nodes(edge[0])
count2 = count_nodes(edge[1])

print(f'Part 1 {count1*count2}')
