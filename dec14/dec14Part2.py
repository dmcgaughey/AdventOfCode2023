import numpy as np


def roll_N(Matrix):
    for col in range(Matrix.shape[1]):
        squares = np.where(Matrix[:, col] == 2)[0]

        if squares.size == 0:
            numRound = np.sum(Matrix[:, col] == 1)
            Matrix[:numRound, col] = 1
            Matrix[numRound:, col] = 0
        else:
            if (squares[-1] < Matrix.shape[0] - 1):
                squares = np.append(squares, Matrix.shape[0])

            squares = squares[-1::-1]
            for sqcnt in range(len(squares) - 1):
                sq1 = squares[sqcnt + 1]
                sq2 = squares[sqcnt]
                numRound = np.sum(Matrix[sq1:sq2, col] == 1)
                Matrix[sq1 + 1:sq1 + 1 + numRound, col] = 1
                Matrix[sq1 + 1 + numRound:sq2, col] = 0
                # print(Matrix[:,col])

            # Now need to process between the last square rock and 0
            sq2 = squares[-1]
            if (sq2 > 0):
                numRound = np.sum(Matrix[0:sq2, col] == 1)
                Matrix[0:numRound, col] = 1
                Matrix[numRound:sq2, col] = 0
    return Matrix


def spin(Matrix):
    Matrix = roll_N(Matrix)
    Matrix = np.rot90(Matrix, axes=(1, 0))
    Matrix = roll_N(Matrix)
    Matrix = np.rot90(Matrix, axes=(1, 0))
    Matrix = roll_N(Matrix)
    Matrix = np.rot90(Matrix, axes=(1, 0))
    Matrix = roll_N(Matrix)
    Matrix = np.rot90(Matrix, axes=(1, 0))
    return Matrix


## Part 2     Find the weight of rock on a table after spinning a long time
# with open('Dec14test.txt', 'r') as f:
with open('Dec14.txt','r') as f:
    lines = f.readlines()

inMatrix = []
# Need extra \n at end for this to process the last table
# Take care !!!!!!!!!
for line in lines:
    temp = line.strip().replace('O', '1').replace('#', '2').replace('.', '0')
    inMatrix.append(list(temp))

Matrix = np.array(inMatrix, dtype=int)

NUMSPINS = 1000  # 1000000000  # Probably better to look for pattern than burn computing power
massList = np.zeros([NUMSPINS, ], dtype=int)
for cnt in range(NUMSPINS):
    Matrix = spin(Matrix)
    mass = np.sum(np.sum(Matrix == 1, axis=1) * np.arange(Matrix.shape[0], 0, -1))
    #if cnt >= 100:
    massList[cnt] = mass
    print(f'Cnt: {cnt+1}  Mass:{mass}')

# Search for a repeating sequence (pattern) in the numbers
# Wait a while for it stabalize
test100 = np.where(massList == massList[100])
test101 = np.where(massList == massList[101])
diff100 = np.diff(test100, 1)
diff101 = np.diff(test101, 1)

for r in range(Matrix.shape[0]):
    s = ''.join(str(Matrix[r, :]))
    print(s)

print(f'Mass: {mass}')
pred = massList[((1000000000-1-110)%14 +110)]
print(f'Prediction {pred}')
# Find all the square rock # = 2
