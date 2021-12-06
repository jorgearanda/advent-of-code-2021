from loader import load_strs


class Diagram:
    def __init__(self, lines):
        self.lines = lines
        self.cells = [
            [0 for _ in range(max(max(line.x1, line.x2) for line in lines) + 1)]
            for _ in range(max(max(line.y1, line.y2) for line in lines) + 1)
        ]
        self.populate_cells()

    def populate_cells(self):
        for line in self.lines:
            self.process_line(line)

    def process_line(self, line):
        if line.is_horizontal():
            for i in range(min(line.x1, line.x2), max(line.x1, line.x2) + 1):
                self.cells[line.y1][i] += 1
        if line.is_vertical():
            for j in range(min(line.y1, line.y2), max(line.y1, line.y2) + 1):
                self.cells[j][line.x1] += 1

    def overlaps(self):
        return sum(cell > 1 for row in self.cells for cell in row)


class DiagonalDiagram(Diagram):
    def process_line(self, line):
        super(DiagonalDiagram, self).process_line(line)
        if not line.is_orthogonal():
            for i, j in list(
                zip(
                    range(line.x1, line.x2 + line.x_step, line.x_step),
                    range(line.y1, line.y2 + line.y_step, line.y_step),
                )
            ):
                self.cells[j][i] += 1


class Line:
    def __init__(self, x1, y1, x2, y2):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_step = 1 if x2 > x1 else -1
        self.y_step = 1 if y2 > y1 else -1

    def is_horizontal(self):
        return self.y1 == self.y2

    def is_vertical(self):
        return self.x1 == self.x2

    def is_orthogonal(self):
        return self.is_horizontal() or self.is_vertical()


def parse_input(lines):
    return [
        Line(*[int(coord) for part in line.split(" -> ") for coord in part.split(",")])
        for line in lines
    ]


if __name__ == "__main__":
    lines = parse_input(load_strs("inputs/day05.txt"))
    print(f"Part 1: {Diagram(lines).overlaps()}")
    print(f"Part 2: {DiagonalDiagram(lines).overlaps()}")


# -- Tests --
fixture = [
    "0,9 -> 5,9",
    "8,0 -> 0,8",
    "9,4 -> 3,4",
    "2,2 -> 2,1",
    "7,0 -> 7,4",
    "6,4 -> 2,0",
    "0,9 -> 2,9",
    "3,4 -> 1,4",
    "0,0 -> 8,8",
    "5,5 -> 8,2",
]


def test_horizontal_line():
    h = Line(3, 1, 1, 1)
    assert h.x1 == 3
    assert h.is_horizontal()
    assert not h.is_vertical()
    assert h.is_orthogonal()


def test_vertical_line():
    v = Line(5, 100, 5, 1)
    assert v.y1 == 100
    assert not v.is_horizontal()
    assert v.is_vertical()
    assert v.is_orthogonal()


def test_diagram():
    h = Line(3, 1, 1, 1)
    v = Line(5, 100, 5, 1)
    d = Diagram([h, v])
    assert len(d.cells) == 101
    assert len(d.cells[0]) == 6


def test_parse_input():
    lines = parse_input(fixture)
    assert len(lines) == 10
    assert lines[9].x1 == 5
    assert lines[9].y2 == 2


def test_part_1():
    assert Diagram(parse_input(fixture)).overlaps() == 5


def test_part_2():
    assert DiagonalDiagram(parse_input(fixture)).overlaps() == 12
