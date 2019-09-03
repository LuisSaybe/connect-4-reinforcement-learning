import itertools

class Environment:
    EMPTY = 0
    AGENT = 1
    ADVERSARY = 2
    CONNNECTION_MAGNITUDE = 4

    def __init__(self):
        self.board = [ [ Environment.EMPTY ] * 7 for row in range(6)]

    def getAvailableActions(self):
        result = []

        for index in range(len(self.board[-1])):
            point = self.board[-1][index]

            if point == Environment.EMPTY:
                result.append(index)

        return result

    def inBounds(self, x, y):
        return x > 0 and y > 0 and x < len(self.board) and y < len(self.board[x])

    def areInBounds(self, points):
        for (x, y) in points:
            if not self.inBounds(x, y):
                return False

        return True

    def areAllEqual(self, points, target):
        return len(list(filter(lambda point: self.board[point[0]][point[1]] == target, points))) == len(points)


    def collectAlongVector(self, magnitude, x, y, dx, dy):
        return [ (x + dx * index, y + dy * index) for index in range(magnitude) ]

    def getState(self):
        result = []

        for row in self.board:
            result.extend(row)
        return result

    def connects(self, x, y, player):
        magnitude_list = list(range(Environment.CONNNECTION_MAGNITUDE))
        verticals = [
            self.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x - i,
                y,
                1,
                0
            ) for i in magnitude_list
        ]
        horizontals = [
            self.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x,
                y - i,
                0,
                1
            ) for i in magnitude_list
        ]
        diagnol_top_left_to_bottom_right = [
            self.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x - Environment.CONNNECTION_MAGNITUDE,
                y - Environment.CONNNECTION_MAGNITUDE, 1, 1
            ) for i in magnitude_list
        ]
        diagnol_bottom_left_to_top_right = [
            self.collectAlongVector(
                Environment.CONNNECTION_MAGNITUDE,
                x - Environment.CONNNECTION_MAGNITUDE,
                y - Environment.CONNNECTION_MAGNITUDE,
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

        for vector in filter(lambda vector: self.areInBounds(vector), all_vectors):
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
