import random


class Agent:
    def __init__(self, rmx_file: str = "rmx.txt", path_presenter=None):
        self.rmx_file = rmx_file
        self.R = []
        self.Q = []
        self.path_presenter = path_presenter
        self.loadR_matrix()
        self.initQ()

    def loadR_matrix(self):

        with open("rmx.txt", "r") as f:
            n = int(f.readline().strip())
            self.R = [[-1 for i in range(n)] for j in range(n)]
            for line in f.readlines():
                i, j, w = list(map(lambda x: int(x), line.split(" ")))
                self.R[i][j] = w

    def initQ(self):
        self.Q = [[i if i > 0 else 0 for i in line] for line in self.R]

    def all_moves_identical(self, moves):
        moves_inv = {v: k for k, v in moves.items}

    def findpath(self, initPos):
        currentPos = initPos
        learnRate = 0.8
        stepCounter = 0
        maxSteps = 1000
        finalMet = False
        vertex_traverse = []
        while not finalMet and stepCounter < maxSteps:
            vertex_traverse.append(currentPos)
            stepCounter += 1
            # get possible move from R[currentPos]
            possMoves = [(ix, i) for ix, i in enumerate(self.R[currentPos]) if i > -1]
            possMoves.sort(key=lambda k: k[1], reverse=True)
            betterMoveWeight = possMoves[0][1]
            possMoves = list(filter(lambda k: k[1] == betterMoveWeight, possMoves))
            # determine random required
            x = random.randint(0, len(possMoves) - 1)
            nextMovePos, nextMovePrize = possMoves[x]
            self.Q[currentPos][nextMovePos] = round(
                self.R[currentPos][nextMovePos] + learnRate * max(self.Q[nextMovePos])
            )
            finalMet = currentPos == nextMovePos
            currentPos = nextMovePos
        if path_presenter is not None:
            path_presenter(vertex_traverse)

    def get_possible_nodes(self):
        return list(range(len(self.R)))


def path_presenter(pth):
    print(f"=> Traverse Path => {pth}")


agent = Agent(path_presenter=path_presenter)

initPosSet = agent.get_possible_nodes()

while len(initPosSet) > 0:
    init_ix = random.randint(0, len(initPosSet) - 1)
    initPos = initPosSet[init_ix]
    del initPosSet[init_ix]
    agent.findpath(initPos)

    for l in agent.Q:
        print(l)
    print("-" * 40)
