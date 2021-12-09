from loader import load_strs


class Heightmap:
    def __init__(self, lines):
        self.cells = [
            [Cell(i, j, cell, self) for i, cell in enumerate(line)]
            for j, line in enumerate(lines)
        ]
        self.basins = []
        for row in self.cells:
            for cell in row:
                cell.scout()

        self.calc_low_points()
        self.calc_risk()
        self.calc_basins()
        self.calc_largest_basins_value()

    def calc_low_points(self):
        self.low_points = [cell for row in self.cells for cell in row if cell.low_point]

    def calc_risk(self):
        self.risk = sum(cell.value for cell in self.low_points) + len(self.low_points)

    def calc_basins(self):
        self.basins = [[]]
        to_fill = set()
        for low_point in self.low_points:
            if low_point.in_basin:
                continue
            to_fill.add(low_point)
            while to_fill:
                cell = to_fill.pop()
                cell.in_basin = True
                self.basins[-1].append(cell)
                to_fill.update(
                    [
                        neighbour
                        for neighbour in cell.neighbours
                        if not neighbour.in_basin and not neighbour.basin_edge
                    ]
                )
            self.basins.append([])

    def calc_largest_basins_value(self):
        sizes = sorted(len(basin) for basin in self.basins)
        self.largest_basins_value = sizes[-1] * sizes[-2] * sizes[-3]


class Cell:
    def __init__(self, x, y, value, heightmap):
        self.x = x
        self.y = y
        self.value = int(value)
        self.heightmap = heightmap
        self.in_basin = False
        self.neighbours = None
        self.low_point = None
        self.basin_edge = self.value == 9

    def scout(self):
        self.calc_neighbours()
        self.calc_is_low_point()

    def calc_neighbours(self):
        self.neighbours = []
        if self.x > 0:
            self.neighbours.append(self.heightmap.cells[self.y][self.x - 1])
        if self.x < len(self.heightmap.cells[self.y]) - 1:
            self.neighbours.append(self.heightmap.cells[self.y][self.x + 1])
        if self.y > 0:
            self.neighbours.append(self.heightmap.cells[self.y - 1][self.x])
        if self.y < len(self.heightmap.cells) - 1:
            self.neighbours.append(self.heightmap.cells[self.y + 1][self.x])

    def calc_is_low_point(self):
        self.low_point = all(n.value > self.value for n in self.neighbours)


if __name__ == "__main__":
    heightmap = Heightmap(load_strs("inputs/day09.txt"))
    print(f"Part 1: {heightmap.risk}")
    print(f"Part 2: {heightmap.largest_basins_value}")


# -- Tests --
fixture = [
    "2199943210",
    "3987894921",
    "9856789892",
    "8767896789",
    "9899965678",
]


def test_part_1():
    h = Heightmap(fixture)
    assert len(h.low_points) == 4
    assert h.risk == 15


def test_part_2():
    h = Heightmap(fixture)
    assert h.largest_basins_value == 1134
