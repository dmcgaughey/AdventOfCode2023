import numpy as np

# Make pathMap a global variable
map = []
pathMap = []

def test_R(pos,pastdir):
    if pos[1] < map.shape[1] - 1:
        return not ( 'R' in pathMap[pos[0], pos[1]+1] )
    else:
        return False

def test_L(pos,pastdir):
    if pos[1] > 0:
        return not ( 'L' in pathMap[pos[0], pos[1]-1] )
    else:
        return False

def test_D(pos, pastdir):
    if pos[0] < map.shape[0] - 1:
        return not ( 'D' in pathMap[pos[0]+1, pos[1]] )
    else:
        return False

def test_U(pos, pastdir):
    if pos[0] > 0:
        return not ('U' in pathMap[pos[0] - 1, pos[1]])
    else:
        return False

def add_direction(pos,dir):
    if not dir in pathMap[pos[0], pos[1]]:
        pathMap[pos[0], pos[1]] += dir

def find_path(pos, direction):
    curPt = pathMap[pos[0], pos[1]]
    mapVal = map[pos[0], pos[1]]
    while (1):
        if pos[0] == 7 and pos[1] == 46:
            print('Here')

        if not direction in pathMap[pos[0], pos[1]]:
            pathMap[pos[0], pos[1]] += direction
        elif map[pos[0], pos[1]] == '.':
            return      # in a loop

        match direction:
            case 'U':
                match map[pos[0], pos[1]]:
                    case '-':       # Splitter: Splits beam both directions
                        # Splits beam right and left
                        if test_R(pos,direction):              # Check if you can move right
                            find_path([pos[0], pos[1] + 1], 'R')

                        if test_L(pos,direction):
                            find_path([pos[0], pos[1] - 1], 'L')
                        break
                    case '/':           # Mirror
                        # Check out the path to the right
                        if test_R(pos,direction):  # Check if you can move right
                            find_path([pos[0], pos[1] + 1], 'R')
                        break
                        # Doing nothing continues up
                    case '\\':          # Mirror
                        # Check out the left path
                        if test_L(pos,direction):
                            find_path([pos[0], pos[1] - 1], 'L')
                        break

                    case _:        #  '|' and '.' do same thing
                        if pos[0] > 0:
                            pos[0] -= 1
                            if map[pos[0],pos[1]] == 'U':
                                break       # in a loop
                        else:
                            break


            case 'D':
                match map[pos[0], pos[1]]:
                    case '-':
                        # Splits beam right and left
                        if test_R(pos,direction):  # Check if you can move right
                            find_path([pos[0], pos[1] + 1], 'R')

                        if test_L(pos,direction):
                            find_path([pos[0], pos[1] - 1], 'L')
                        break
                    case '/':
                        # Check out the left path
                        if test_L(pos,direction):
                            find_path([pos[0], pos[1] - 1], 'L')
                        break
                    case '\\':
                        # Check out the path to the right
                        if test_R(pos,direction):  # Check if you can move right
                            find_path([pos[0], pos[1] + 1], 'R')
                        break
                    case _:  #  '|' and '.' do same thing
                        ## Already added 'D'             pathMap[pos[0], pos[1]] += 'D'
                        if pos[0] < map.shape[0]-1:
                            pos[0] += 1
                            if map[pos[0],pos[1]] == 'D':
                                break       # in a loop
                        else:
                            break

            case 'R':
                match map[pos[0], pos[1]]:
                    # case '.':   # case '-':
                    case '|':
                        # Splits beam UP and DOWN
                        if test_U(pos,direction):  # Check if you can move UP
                            find_path([pos[0]-1, pos[1]], 'U')

                        if test_D(pos,direction):
                            find_path([pos[0]+1, pos[1]], 'D')
                        break
                    case '/':
                        # Check out the path UP
                        if test_U(pos,direction):  # Check if you can move right
                            find_path([pos[0]-1, pos[1]], 'U')
                        break
                        # Doing nothing continues up
                    case '\\':
                        # Check out the path DOWN                       0
                        if test_D(pos,direction):
                            find_path([pos[0] + 1, pos[1]], 'D')
                        break
                    case _:     # '.', '-'  continue RIGHT
                        # pathMap[pos[0],pos[1]] += 'R'
                        if pos[1] < map.shape[1] - 1:
                            pos[1] += 1
                            if map[pos[0],pos[1]] == 'R':
                                break       # in a loop
                        else:
                            break

            case 'L':
                match map[pos[0], pos[1]]:
                    # case '.':   # case '-':
                    case '|':
                        # Splits beam UP and DOWN
                        if test_U(pos,direction):  # Check if you can move right
                            find_path([pos[0] - 1, pos[1]], 'U')
                        if test_D(pos,direction):
                            find_path([pos[0] + 1, pos[1]], 'D')
                        break
                    case '/':
                        # Check out the path DOWN                       0
                        if test_D(pos,direction):
                            find_path([pos[0] + 1, pos[1]], 'D')
                        break
                        # Doing nothing continues up
                    case '\\':
                        # Check out the path UP
                        if test_U(pos,direction):  # Check if you can move right
                            find_path([pos[0] - 1, pos[1]], 'U')
                        break
                    case _:  # '.', '-'  continue RIGHT
                        if pos[1] <= 0:
                            break
                        else:
                            pos[1] -= 1
                            if map[pos[0],pos[1]] == 'L':
                                break          # Already moved left through the next square


def textDebug():
    printPath = np.copy(pathMap)
    counts = np.char.str_len(pathMap)
    printPath [:,:] = np.char.add(map[:,:],' ')
    printPath[counts>=2] = np.char.add(map[counts>=2] , counts[counts>=2].astype(str))
    printPath[counts==1] = np.char.add(map[counts==1], pathMap[counts==1])

    printPath = np.char.replace(printPath,'R','>')
    printPath = np.char.replace(printPath,'L','<')
    printPath = np.char.replace(printPath,'U','^')
    printPath = np.char.replace(printPath,'D','v')


    outStr = []
    for cnt in range(printPath.shape[0]):
        outStr.append(''.join(printPath[cnt,:]))
    return outStr

def textPath():
    printPath = np.copy(map)    # One char per element is fine
    counts = np.char.str_len(pathMap)
    printPath[counts>=2] = counts[counts>=2].astype(str)
    printPath[counts==1] = pathMap[counts==1]

    printPath[map=='\\'] = '\\'
    printPath[map=='/'] = '/'
    printPath[map == '|'] = '|'
    printPath[map == '-'] = '='
    printPath = np.char.replace(printPath,'R','>')
    printPath = np.char.replace(printPath,'L','<')
    printPath = np.char.replace(printPath,'U','^')
    printPath = np.char.replace(printPath,'D','v')

    printPath[counts==0] = '.'

    outStr = []
    for cnt in range(printPath.shape[0]):
        outStr.append(''.join(printPath[cnt,:]))
    return outStr

## Part 1     Find paths through maze
# with open('Dec16test.txt', 'r') as f:
with open('Dec16.txt','r') as f:
    lines = f.readlines()

inMatrix = []
for line in lines:
    inMatrix.append(list(line.replace('\n','')))


map = np.array(inMatrix, dtype=str)
temp = ['          ']*map.size
pathMap = np.array(temp).reshape(map.shape)
pathMap[:,:] = ''

find_path([0,0], 'R')


numSquares = np.sum(pathMap != '')


outPath = textPath()

for l in outPath:
    print(l)

f2 = open('Outpath.txt', 'w')
for l in outPath:
    f2.writelines(l+'\n')
f2.close()

numSquares = np.sum(pathMap != '')

print(f'NumSquares : {numSquares}')
