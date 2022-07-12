import string
from math import inf

from exceptions.exceptions import MazeException, GridGeneratorException


class GridGenerator:
    WALL = "W"
    MOVE = "M"
    LIMIT = 26

    def __init__(self, grid_size, walls):
        self._cc = CoordinatesConverter()
        self._walls = {self._cc.vocal_2_numeric(wall): self.WALL for wall in walls}
        self.width, self.height = self.get_size(grid_size)

    def get_size(self, grid_size):
        width, height = [int(x) for x in grid_size.split("x")]
        if width > self.LIMIT or height > self.LIMIT:
            raise GridGeneratorException("Maze should be no bigger than 26")
        return width, height

    def generate_new_grid(self):
        return [
            [self._walls.get((j, i), self.MOVE) for i in range(self.width)]
            for j in range(self.height)
        ]


class MazeGame:
    def __init__(self, entrance, grid_size, walls):
        self.cc = CoordinatesConverter()
        self.gg = GridGenerator(grid_size, walls)

        self.grid = self.gg.generate_new_grid()
        self.entrance = self.cc.vocal_2_numeric(entrance)
        self.target = self.get_target()

    def get_target(self):
        col = self.gg.height - 1
        # start from down right to down left
        for row in range(self.gg.width - 1, -1, -1):
            if self.grid[col][row] != self.gg.WALL:
                return col, row
        raise MazeException("Target over grid limit")

    def generate_graph(self, i, j, graph):
        if (
            i < 0
            or j < 0
            or i >= len(self.grid)
            or j >= len(self.grid[0])
            or self.grid[i][j] == self.gg.WALL
        ):
            return
        k = (i, j)
        if k not in graph:
            graph[k] = {}
        if (i - 1, j) in graph:
            graph[(i - 1, j)][k] = 1
            graph[k][(i - 1, j)] = 1
        if (i + 1, j) in graph:
            graph[(i + 1, j)][k] = 1
            graph[k][(i + 1, j)] = 1
        if (i, j - 1) in graph:
            graph[(i, j - 1)][k] = 1
            graph[k][(i, j - 1)] = 1
        if (i, j + 1) in graph:
            graph[(i, j + 1)][k] = 1
            graph[k][(i, j + 1)] = 1
        self.grid[i][j] = self.gg.WALL
        self.generate_graph(i + 1, j, graph)
        self.generate_graph(i - 1, j, graph)
        self.generate_graph(i, j + 1, graph)
        self.generate_graph(i, j - 1, graph)

    def search(self, source, graph, costs, parents, shortest=True):
        next_node = source
        while next_node != self.target:
            for neighbor in graph[next_node]:
                dif = (
                    costs[next_node] < costs[neighbor]
                    if shortest
                    else costs[next_node] > costs[neighbor]
                )
                if graph[next_node][neighbor] + dif:
                    costs[neighbor] = graph[next_node][neighbor] + costs[next_node]
                    parents[neighbor] = next_node
                graph[neighbor].pop(next_node)
            costs.pop(next_node)

            if not costs:
                raise MazeException("No path found")
            next_node = (
                min(costs, key=costs.get) if shortest else max(costs, key=costs.get)
            )
        return parents

    def bpedal(self, source, search_result):
        node, bpath = self.target, [self.target]
        while node != source:
            bpath.append(search_result[node])
            node = search_result[node]

        return [self.cc.numeric_2_vocal(*bpath[-i - 1]) for i in range(len(bpath))]

    def shortest_path(self, shortest_path=True):
        """
        :param shortest_path: Param indicating which type of path the user needs to get, default is True
        :return: Path to target
        """
        graph = {}
        self.generate_graph(*self.entrance, graph)
        costs = self._generate_cost(graph, shortest_path)
        self.grid = self.gg.generate_new_grid()

        result = self.search(self.entrance, graph, costs, {}, shortest_path)
        return {"path": self.bpedal(self.entrance, result)}

    @staticmethod
    def _generate_cost(graph, shortest=True):
        costs = {j: inf if shortest else -inf for i, j in enumerate(graph)}
        costs[next(iter(graph))] = 0
        return costs


class CoordinatesConverter:
    ALPHABET_AS_LIST = list(string.ascii_lowercase)
    NUMBER_2_LETTER = {i: x.upper() for i, x in enumerate(ALPHABET_AS_LIST)}
    LETTER_2_NUMBER = {x.upper(): i for i, x in enumerate(ALPHABET_AS_LIST)}
    OFFSET = 1

    def vocal_2_numeric(self, vocal_coordinates):
        letter, row = list(vocal_coordinates)
        return self.LETTER_2_NUMBER[letter], int(row) - self.OFFSET

    def numeric_2_vocal(self, x, y):
        return f"{self.NUMBER_2_LETTER[x]}{y + self.OFFSET}"
