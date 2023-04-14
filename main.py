import random

def loadR_matrix():
    R = []
    with open("rmx.txt", "r") as f:
        n = int(f.readline().strip())
        R = [[-1 for i in range(n)] for j in range(n)]
        for line in f.readlines():
            i,j,w = list(map(lambda x: int(x), line.split(" ")))
            R[i][j] = w
    return R


def initQ(R):
    Q = [[i if i > 0 else 0 for i in line] for line in R]
    return Q

def all_moves_identical(moves):
    moves_inv = {v:k for k,v in moves.items}


def path_presenter(pth):
    print(f"= Traverse Path => {pth}")

R = loadR_matrix()
Q = initQ(R)


def findpath(Q, initPos, path_presenter = None):
    currentPos = initPos
    learnRate = 0.8
    stepCounter = 0
    maxSteps = 1000
    finalMet = False
    vertex_traverse = []
    while not finalMet and stepCounter < maxSteps:
        vertex_traverse.append(currentPos)
        stepCounter +=1
        # get possible move from R[currentPos]
        possMoves = [(ix,i) for ix,i in enumerate(R[currentPos]) if i > -1]
        possMoves.sort(key=lambda k: k[1], reverse=True)
        betterMoveWeight = possMoves[0][1]
        possMoves = list(filter(lambda k: k[1] == betterMoveWeight, possMoves))
        # determine random required
        x = random.randint(0, len(possMoves)-1)
        nextMovePos, nextMovePrize = possMoves[x]
        Q[currentPos][nextMovePos] = round(R[currentPos][nextMovePos] + learnRate * max(Q[nextMovePos]))
        finalMet = currentPos == nextMovePos
        currentPos = nextMovePos
    if path_presenter is not None:
        path_presenter(vertex_traverse)
    return Q

initPosSet = list(range(len(R)))

while len(initPosSet) > 0:
    init_ix = random.randint(0, len(initPosSet) - 1)
    initPos = initPosSet[init_ix]
    del initPosSet[init_ix]
    # print(f"Start position: {initPos}")
    findpath(Q, initPos, path_presenter)

    #
    for l in Q:
        print(l)
    print("-" * 40)