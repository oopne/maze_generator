class UnionFind:
    def __init__(self, count):
        self._parents = list(range(count))
        self._sizes = [1] * count

    def find(self, node):
        if node == self._parents[node]:
            return node
        self._parents[node] = self.find(self._parents[node])
        return self._parents[node]

    def union(self, node1, node2):
        node1 = self.find(node1)
        node2 = self.find(node2)
        if self._sizes[node1] > self._sizes[node2]:
            node1, node2 = node2, node1
        self._parents[node1] = node2
        self._sizes[node2] += self._sizes[node1]


class Grid:
    __wall = '🔳'
    __space = '⬛'
    __path = '⬜'
    __start = '🟩'
    __finish = '🛑'
    
    def __init__(self, **kwargs):
        if 'width' in kwargs and 'height' in kwargs:
            width = kwargs['width']
            height = kwargs['height']
            rows = height * 2 + 1
            columns = width * 2 + 1
            self._table = [[Grid.__wall] * columns for i in range(rows)]
            for i in range(height):
                for j in range(width):
                    self.erase_wall(i * 2 + 1, j * 2 + 1)
        elif 'table' in kwargs:
            self._table = kwargs['table']
        else:
            raise ArgumentError('Invalid arguments in constructor')

    def erase_wall(self, row, col):
        self._table[row][col] = Grid.__space

    def mark_cell(self, row, col):
        self._table[row][col] = Grid.__path

    def unmark_cell(self, row, col):
        self._table[row][col] = Grid.__space

    def __str__(self):
        return '\n'.join([''.join(row) for row in self._table])

    def load_from_file(path):
        with open(path) as file:
            func = lambda line: list(line.strip('\n'))
            table = list(map(func, file.readlines()))
        return Grid(table=table)

    def adjacent_walls(self, row, col):
        positions = []
        if row > 1 and self._table[row - 1][col] == Grid.__wall:
            positions.append((row - 1, col))
        if row < len(self._table) - 2 and \
            self._table[row + 1][col] == Grid.__wall:
            positions.append((row + 1, col))
        if col > 1 and self._table[row][col - 1] == Grid.__wall:
            positions.append((row, col - 1))
        if col < len(self._table[0]) - 2 and \
            self._table[row][col + 1] == Grid.__wall:
            positions.append((row, col + 1))
        return positions

    @property
    def height(self):
        return len(self._table)

    @property
    def width(self):
        return len(self._table[0])

    def get_walls(self):
        walls = []
        for i in range(1, len(self._table) - 1):
            for j in range(1, len(self._table[0]) - 1):
                if self._table[i][j - 1] == Grid.__space and \
                    self._table[i][j + 1] == Grid.__space:
                    walls.append(((i, j - 1), (i, j), (i, j + 1)))
                if self._table[i - 1][j] == Grid.__space and \
                    self._table[i - 1][j] == Grid.__space:
                    walls.append(((i - 1, j), (i, j), (i + 1, j)))
        return walls

    def get_cells(self):
        cells = []
        for i in range(1, len(self._table) - 1):
            for j in range(1, len(self._table[0]) - 1):
                if self._table[i][j] == Grid.__space:
                    cells.append((i, j))
        return cells

    def adjacent_cells(self, row, col):
        positions = []
        if self._table[row - 1][col] == Grid.__space:
            positions.append((row - 1, col))
        if self._table[row + 1][col] == Grid.__space:
            positions.append((row + 1, col))
        if self._table[row][col - 1] == Grid.__space:
            positions.append((row, col - 1))
        if self._table[row][col + 1] == Grid.__space:
            positions.append((row, col + 1))
        return positions

    def save(self, path):
        with open(path, 'w') as file:
            file.write(self.__str__())
    
    def mark_start(self, row, col):
        self._table[row][col] = Grid.__start

    def mark_finish(self, row, col):
        self._table[row][col] = Grid.__finish

    def is_cell_empty(self, row, col):
        return 0 <= row < self.height and \
               0 <= col < self.width and \
               self._table[row][col] == Grid.__space


def random_depth_first_search(grid):
    from random import shuffle
    stack = [((1, 1), None),]
    used = set()
    while stack:
        node, wall_to_erase = stack.pop()
        if node in used:
            continue
        used.add(node)
        if wall_to_erase:
            grid.erase_wall(*wall_to_erase)
        walls = grid.adjacent_walls(*node)
        shuffle(walls)
        for wall in walls:
            delta = (wall[0] - node[0], wall[1] - node[1])
            next_node = (node[0] + delta[0] * 2, node[1] + delta[1] * 2)
            if not next_node in used:
                stack.append((next_node, wall))


def random_kruskal(grid):
    from random import shuffle
    height = grid.height
    width = grid.width
    dsu = UnionFind(height * width)
    walls = grid.get_walls()
    shuffle(walls)
    index = lambda node: node[0] * height + node[1]
    for wall in walls:
        node1 = index(wall[0])
        node2 = index(wall[2])
        if dsu.find(node1) != dsu.find(node2):
            dsu.union(node1, node2)
            grid.erase_wall(*wall[1])


def random_binary_tree(grid):
    from random import choice
    nodes = grid.get_cells()
    for node in nodes:
        walls = [wall for wall in grid.adjacent_walls(*node) \
                 if wall[0] < node[0] or wall[1] < node[1]]
        if walls:
            grid.erase_wall(*choice(walls))


def mark_path(grid, start, finish):
    used = set()
    found = False
    def find_path(node):
        nonlocal found
        nonlocal finish
        used.add(node)
        if node == finish:
            found = True
            return
        for next_node in grid.adjacent_cells(*node):
            if not next_node in used and not found:
                grid.mark_cell(*next_node)
                find_path(next_node)
                if found:
                    return
                grid.unmark_cell(*next_node)
    grid.mark_start(*start)
    find_path(start)
    grid.mark_finish(*finish)
