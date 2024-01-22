# import pandas as pd
import numpy as np
import sys
import re
sys.setrecursionlimit(141 * 141)

# Use DICT as structure
# [ len, pos=[x,y],dir,runlen]
mymap = []
# mypath = []
destination = ()
bestpath = []
searched = []
toSearchQ = []
global EXTRA_PATH

bestDistance = np.array([0])
def updateBestDistance(node):
    global bestDistance

    if bestDistance.shape != mymap.shape:
        bestDistance = np.zeros(mymap.shape) + np.sum(mymap)+1
    pos = node['pos']
    if node['len'] < bestDistance[pos[0]][pos[1]]:
        bestDistance[pos[0]][pos[1]] = node['len']
    return

def getBestDistance(node):
    pos = node['pos']
    return bestDistance[pos[0]][pos[1]]

def show_path(path_str):
    newmap = mymap.astype(str)

    pos = [0, 0]
    newpos=pos
    path_str = path_str[1:]
    for c in path_str:
        match c:
            case 'U':
                char = '^'
                newpos[0] = pos[0] - 1
            case 'D':
                char = 'v'
                newpos[0] = pos[0] + 1
            case 'R':
                char = '>'
                newpos[1] = pos[1] + 1
            case 'L':
                char = '<'
                newpos[1] = pos[1] - 1
        newmap[node['pos'][0], node['pos'][1]] = char

    print('\n\n')
    for cnt in range(newmap.shape[0]):
        temp = ''.join(newmap[cnt, :])
        print(temp)

# def show_path(inpath):
#     newmap = mymap.astype(str)
#     for node in inpath:
#         if not node:
#             break
#         dir = node['path'][-1]
#         if dir == 'R':
#             char = '>'
#         elif dir == 'L':
#             char = '<'
#         elif dir == 'U':
#             char = '^'
#         elif dir == 'D':
#             char = 'v'
#         else:
#             continue
#         newmap[node['pos'][0], node['pos'][1]] = char
#
#     print('\n\n')
#     for cnt in range(newmap.shape[0]):
#         temp = ''.join(newmap[cnt, :])
#         print(temp)


boolMap = np.array([0])
def alreadyinpath(path_str):
    global boolMap
    if boolMap.shape != mymap.shape:
        boolMap = np.zeros(mymap.shape,dtype=bool)

    boolMap[:,:] = False
    boolMap[0,0] = True
    pos = [0,0]
    path_str = path_str[1:]
    for c in path_str:
        match c:
            case 'U': pos[0] -= 1
            case 'D': pos[0] += 1
            case 'R': pos[1] += 1
            case 'L': pos[1] -= 1
        if boolMap[pos[0],pos[1]]:
            return True
        else:
            boolMap[pos[0], pos[1]] = True
    return False


def print_searched_path(node):
    return

def get_turn_history(path_str):
    turn_hist = re.sub(r"(.)\1+", r"\1",path_str)
    if len (turn_hist)>4: turn_hist = turn_hist[-4:]
    return turn_hist

# def already_searched(node):
#     # Step 0: Get the up to 4 char key of the turn history
#     turn_hist = get_turn_history(node['path'])
#     # Step 1: Test if sequence of turns has already been searched
#     if node:
#         sList = searched[node['pos'][0]][node['pos'][1]]
#         for s in sList:
#             if  s['indirs'] == turn_hist:
#                 return True
#     return False

# def get_searched_node(node):
#     # Return the dictionary in searched that matches this node location and indir string
#     # Step 0: Get the up to 4 char key of the turn history
#     turn_hist = get_turn_history(node['path'])
#     # Step 1: Test if sequence of turns has already been searched
#     if node:
#         sList = searched[node['pos'][0]][node['pos'][1]]
#         for s in sList:
#             if s['indirs'] == turn_hist:
#                 return s
#     return []


def get_searched_path(node):
    # Step 0: Get the up to 4 char key of the turn history
    turn_hist = get_turn_history(node['path'])
    # Step 1: Test if sequence of turns has already been searched
    if node:
        sList = searched[node['pos'][0]][node['pos'][1]]
        for s in sList:
            if s['indirs'] == turn_hist:
                break
        else:
            return []

    # Step 2: Ensure that new path is valid (ie don't have 4 of same char in row
    new_path = node['path'] + s['outdirs']
    if re.search(r'(.)\1{3}', new_path) == None:
        new_len = node['len'] + s['len2end']
        return {'len':new_len, 'path':new_path}
    return []


def updatesearched(node):       # Node contains a length and a path
    # Update the searched array but only replace elements that are not present or smaller than the current
    # distance for indir string of 4 chars and runlen
    global searched
    pathstr = node['path'] + ' ' # Add char for position 12,12 is processed
    pos = [0,0]
    len2end = node['len']
    indirs = pathstr[0]
    outdirs = pathstr      # Next text for (0,0) as it is processed before incrementing

    for c in pathstr[1:]:      # Start processing at move to second point as first point is (0,0)
        if pos != [0,0]:
            len2end -= mymap[pos[0], pos[1]]

        if len2end <0:
            print('Error')

        if indirs[-1] != outdirs[0]:
            indirs = (indirs + outdirs[0]) if len(indirs)<4 else (indirs[1:] + outdirs[0])
        outdirs = outdirs[1:]
        newentry = { 'len2end': len2end, 'indirs': indirs, 'outdirs': outdirs}

        # Update the searched array
        if not searched[pos[0]][pos[1]]:
            searched[pos[0]][pos[1]] = [newentry]
        else:
            sList = searched[pos[0]][pos[1]]
            for cnt in range(len(sList)):
                if indirs == sList[cnt]['indirs']:
                    if sList[cnt]['len2end'] > len2end:
                        sList[cnt] = newentry
                    break
            else:
                searched[pos[0]][pos[1]].append(newentry)

        match c:
            case 'U':
                pos[0] -= 1
            case 'D':
                pos[0] += 1
            case 'R':
                pos[1] += 1
            case 'L':
                pos[1] -= 1
            case ' ':
                break
    return


# def get_path_from_pathstr(path_str, pos=(0,0), len=0):
#     newpath = []
#     tpath= path_str[0]
#     path_str = path_str[1:]
#     pos = list(pos)
#
#     newpath.append({'pos':tuple(pos), 'len':len, 'path':tpath})
#
#     out_str = path_str
#     for c in path_str:
#         match c:
#             case 'U':  pos[0] -= 1
#             case 'D':  pos[0] += 1
#             case 'R':  pos[1] += 1
#             case 'L':  pos[1] -= 1
#         len += mymap[pos[0],pos[1]]
#         tpath += out_str[0]
#         out_str = out_str[1:]
#         newpath.append({'pos': tuple(pos), 'len': len, 'path': tpath})
#     return newpath

def lowestlength(node):
    # The Manhattan distance plus your current weight is the lowest possible length to the end
    lowestlen = node['len'] + (destination[0] - node['pos'][0]) + (destination[1] - node['pos'][1])
    return lowestlen

def mdistance(pos):
    return (destination[0] - node['pos'][0]) + (destination[1] - node['pos'][1])

def next_square(pos, newdir, pastdir, runlen, len, path):
    # Check for condition to turn, or stop searching this direction
    if newdir == pastdir and runlen >= 3:
        return []

    backtrack = (newdir == 'R' and pastdir == 'L') or (newdir == 'D' and pastdir == 'U') \
                or (newdir == 'L' and pastdir == 'R') or (newdir == 'U' and pastdir == 'D')
    if backtrack:
        return []

    backtrackonedge = (pos[0] == 0 and newdir == 'L') or (pos[0] == mymap.shape[0] - 1 and newdir == 'L') \
                      or (pos[1] == 0 and newdir == 'U') or (pos[0] == mymap.shape[0] - 1 and newdir == 'U')
    if backtrackonedge:
        return []

    temp_pos = list(pos)
    match newdir:
        case 'U':
            temp_pos[0] -= 1
            delta = 1
        case 'D':
            temp_pos[0] += 1
            delta = -1
        case 'R':
            temp_pos[1] += 1
            delta = -1
        case 'L':
            temp_pos[1] -= 1
            delta = 1

    if temp_pos[0] < 0 or temp_pos[0] > mymap.shape[0] - 1 or temp_pos[1] < 0 or temp_pos[1] > mymap.shape[1] - 1:
        return []

    newPath = path + newdir
    if alreadyinpath(newPath):
        return []

    newlength = mymap[temp_pos[0], temp_pos[1]] + len
    metric = mymap[temp_pos[0],temp_pos[1]] + 1*delta + 10*delta/mdistance(temp_pos)
    return {'pos': tuple(temp_pos), 'len': newlength, 'metric':metric,  'path': newPath}


def findPathGreedy(node, cnt=0):  # node = [len, [x,y], dir, runlen):
    global bestpath, searched       #, mypath

    pos = node['pos']
    path = node['path']
    # length = node['len']

    # Check if you are at the end
    if pos == destination:
        # Update the searched array (it keeps only best path -> no need to worry)
        updatesearched(node)

        if node['len'] < bestpath['len']:
            bestpath = {'len':node['len'], 'path':node['path']}
            best = bestpath['len']
            print(f'New Best {best}')
        return

    # Stop if you need further then the best to get to the end
    if lowestlength(node) >= bestpath['len'] + EXTRA_PATH:
        return

    # Test if you have already searched this square in this direction
    # if  (testnode := get_searched_path(node)):
    #     # temppath = get_path_from_pathstr(testpathstr)
    #     updatesearched(testnode)
    #
    #     if bestpath['len'] > testnode['len']:
    #         # Update bestpath
    #         bestpath = testnode.copy()  #  {'len': testnode['len'], 'path': testnode['path']}
    #         best = bestpath['len']
    #         print(f'New Best {best}')
    #     return  # No further search needed -> use past result

    #####
    ## Actual searching of the 4 directions
    ####
    # Break out variables need to call next_square
    pos = node['pos']
    length = node['len']
    # Calculate the runlen from the path
    temppath = path[::-1]
    runlen = 1
    for c in temppath[1:]:
        if c == path[-1]:
            runlen += 1
        else:
            break

    # potentialdirs = ['R', 'D', 'L', 'U']
    # # potentialdirs = ['D', 'R','L','U']
    # tempnodes = []
    # for newdir in potentialdirs:
    #     if pos == (0, 0):
    #         runlen = 1  # Special case for first square
    #         pastdir = newdir
    #         path = newdir
    #     else:
    #         pastdir = node['path'][-1]
    #     nextSq = next_square(pos, newdir, pastdir, runlen, length, path)
    #     if nextSq:
    #         tempnodes.append(nextSq)
    #
    # # Sort the tempnodes
    # def get_metric(node):
    #     return node.get('metric')
    #
    # def get_dist(node):
    #     return node['pos'][0]**2 + node['pos'][1]**2
    #
    # if tempnodes:
    #     tempnodes.sort(key=get_metric)
    #     numtosearch = len(tempnodes)
    #
    #     for nextnode in tempnodes:
    #         # nextSq = toSearchQ.pop(0)
    #         findPathGreedy(nextnode, cnt + 1)

        # for cnt in range(1,len(tempnodes)):
        #     toSearchQ.append(tempnodes[cnt])
        #     # toSearchQ.insert(0,tempnode)
        #
        # # Didn't push the first square so can run it first
        # nextSq = tempnodes[0]
        # findPathGreedy(nextSq, cnt + 1)

        #toSearchQ.sort(reverse=False, key=get_dist)
        # Now pop nodes (same number as pushed: but necessarily the same nodes)
        # for _ in range(numtosearch-1):
        #     nextSq = toSearchQ.pop()
        #     findPathGreedy(nextSq, cnt + 1)

    potentialdirs = ['R', 'D', 'L', 'U']
    # potentialdirs = ['D', 'R','L','U']
    for newdir in potentialdirs:
        if pos == (0, 0):
            runlen = 1  # Special case for first square
            pastdir = newdir
            path = newdir
        else:
            pastdir = node['path'][-1]
        nextSq = next_square(pos, newdir, pastdir, runlen, length, path)
        if nextSq:
            findPathGreedy(nextSq, cnt + 1)
    return

##################
## Main program
##
##
##
##
##################

with open('dec17Test.txt', 'r') as f:
# with open('dec17.txt', 'r') as f:
    lines = f.readlines()
f.close()

mapList = []
for line in lines:
    mapList.append(list(line.strip()))

mymap = np.array(mapList, dtype=int)
print(mymap)

srow = [[] for _ in range(mymap.shape[1])]
for cnt in range(mymap.shape[0]):
    searched.append(srow.copy())

destination = (mymap.shape[0] - 1, mymap.shape[1] - 1)
bestpath =  {'len': np.sum(mymap) + 1, 'path': ''}
node = {'pos': (0, 0), 'len': 0, 'path':''}
EXTRA_PATH = int(mymap.size/30*np.mean(mymap))
# mypath.append(node)
findPathGreedy(node)

shortest = bestpath['len']
print(f'Bestpath: {shortest}')
show_path(bestpath['path'])
