from loader import load_strs


class Cavern:
    def __init__(self, lines):
        self.cells = [
            [Cell(i, j, cell, self) for i, cell in enumerate(line)]
            for j, line in enumerate(lines)
        ]
        for row in self.cells:
            for cell in row:
                cell.scout()

    def __str__(self):
        return "".join(
            f"{''.join(str(cell.risk) for cell in row)}\n" for row in self.cells
        )

    def calc_risk(self):
        # First pass
        for row in self.cells:
            for cell in row:
                if cell.x == 0 and cell.y == 0:
                    cell.total_risk = 0
                elif cell.x > 0:
                    cell.total_risk = (
                        cell.risk + self.cells[cell.y][cell.x - 1].total_risk
                    )
                else:
                    cell.total_risk = cell.risk + self.cells[cell.y - 1][0].total_risk

        changes = True
        while changes:
            changes = False
            for row in self.cells:
                for cell in row:
                    if any(
                        neighbour.total_risk + cell.risk < cell.total_risk
                        for neighbour in cell.neighbours
                    ):
                        changes = True
                        cell.total_risk = (
                            min(neighbour.total_risk for neighbour in cell.neighbours)
                            + cell.risk
                        )

    def risk_bottom_right(self):
        self.calc_risk()
        return self.cells[-1][-1].total_risk

    def print_total_risk(self):
        for row in self.cells:
            for cell in row:
                print(f"{cell.total_risk:4}", end="")
            print()
        print()


class Cell:
    def __init__(self, x, y, risk, cavern):
        self.x = x
        self.y = y
        self.risk = int(risk)
        self.total_risk = None
        self.cavern = cavern
        self.neighbours = None

    def scout(self):
        self.top_edge = self.y == 0
        self.bottom_edge = self.y == len(self.cavern.cells) - 1
        self.left_edge = self.x == 0
        self.right_edge = self.x == len(self.cavern.cells[self.y]) - 1
        self.neighbours = []

        # Left column
        if not self.left_edge:
            self.neighbours.append(self.cavern.cells[self.y][self.x - 1])

        # Middle column
        if not self.top_edge:
            self.neighbours.append(self.cavern.cells[self.y - 1][self.x])
        if not self.bottom_edge:
            self.neighbours.append(self.cavern.cells[self.y + 1][self.x])

        # Right column
        if not self.right_edge:
            self.neighbours.append(self.cavern.cells[self.y][self.x + 1])


def make_big_cavern_lines(lines):
    res = []
    for j in range(5):
        for line in lines:
            big_line = ""
            for i in range(5):
                for char in line:
                    big_line += str(((int(char) - 1 + i + j) % 9) + 1)
            res.append(big_line)
    return res


if __name__ == "__main__":
    cavern = Cavern(load_strs("inputs/day15.txt"))
    print(f"Part 1: {cavern.risk_bottom_right()}")
    big_cavern = Cavern(make_big_cavern_lines(load_strs("inputs/day15.txt")))
    print(f"Part 2: {big_cavern.risk_bottom_right()}")


# -- Tests --
fixture = [
    "1163751742",
    "1381373672",
    "2136511328",
    "3694931569",
    "7463417111",
    "1319128137",
    "1359912421",
    "3125421639",
    "1293138521",
    "2311944581",
]


def test_load():
    cavern = Cavern(fixture)
    assert len(cavern.cells) == 10
    assert len(cavern.cells[0]) == 10
    assert cavern.cells[9][9].risk == 1


def test_part_1():
    cavern = Cavern(fixture)
    assert cavern.risk_bottom_right() == 40


def test_make_big_cavern():
    lines = make_big_cavern_lines(fixture)
    assert len(lines) == 50
    assert len(lines[0]) == 50
    assert lines[0][0] == "1"
    assert lines[10][10] == "3"
    assert lines[20][20] == "5"
    assert lines[30][30] == "7"
    assert lines[40][40] == "9"


def test_part_2():
    cavern = Cavern(make_big_cavern_lines(fixture))
    assert cavern.risk_bottom_right() == 315
