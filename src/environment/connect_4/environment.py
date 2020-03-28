import itertools

class Environment:
    EMPTY = 0
    AGENT = 1
    ADVERSARY = 2
    CONNNECTION_MAGNITUDE = 4
    COLUMNS = 7
    ROWS = 6
    WIN_REWARD = 1
    LOSE_REWARD = -1
    DEFAULT_REWARD = 0

    def __init__(self):
        self.board = [ [ Environment.EMPTY ] * Environment.COLUMNS for row in range(Environment.ROWS)]

    def getAvailableActions(self):
        result = []

        for index in range(len(self.board[-1])):
            point = self.board[-1][index]

            if point == Environment.EMPTY:
                result.append(index)

        return result

    def inBounds(x, y):
        return x >= 0 and y >= 0 and x < Environment.ROWS and y < Environment.COLUMNS

    def areInBounds(points):
        for (x, y) in points:
            if not Environment.inBounds(x, y):
                return False

        return True

    def areAllEqual(self, points, target):
        return len(list(filter(lambda point: self.board[point[0]][point[1]] == target, points))) == len(points)


    def collectAlongVector(magnitude, x, y, dx, dy):
        return [ (x + dx * index, y + dy * index) for index in range(magnitude) ]

    def getState(self):
        result = []

        for row in self.board:
            result.extend(row)
        return result

    def getInBoundVectors(x, y):
        magnitude_list = list(range(Environment.CONNNECTION_MAGNITUDE))

        verticals = [
            Environment.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x - i,
                y,
                1,
                0
            ) for i in magnitude_list
        ]
        horizontals = [
            Environment.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x,
                y - i,
                0,
                1
            ) for i in magnitude_list
        ]
        diagnol_top_left_to_bottom_right = [
            Environment.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x - i,
                y + i,
                1,
                -1
            ) for i in magnitude_list
        ]
        diagnol_bottom_left_to_top_right = [
            Environment.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x - i,
                y - i,
                1,
                1
            ) for i in magnitude_list
        ]

        all_vectors = itertools.chain(
            verticals,
            horizontals,
            diagnol_top_left_to_bottom_right,
            diagnol_bottom_left_to_top_right
        )
        return list(filter(lambda vector: Environment.areInBounds(vector), all_vectors))

    def connects(self, x, y, player):
        for vector in self.IN_BOUNDS_VECTORS[x][y]:
            if self.areAllEqual(vector, player):
                return True
        return False

    def drop(self, column, player):
        for row in range(len(self.board)):
            if self.board[row][column] == Environment.EMPTY:
                self.board[row][column] = player
                return (row, column)

        return None

    def __str__(self):
     rows = map(lambda row: str(row), reversed(self.board))
     return '\n'.join(rows)

Environment.IN_BOUNDS_VECTORS = [ [ None ] * Environment.COLUMNS for row in range(Environment.ROWS)]

for row in range(Environment.ROWS):
    for column in range(Environment.COLUMNS):
        Environment.IN_BOUNDS_VECTORS[row][column] = Environment.getInBoundVectors(row, column)
