from loader import load_strs


class Paper:
    def __init__(self, coords, folds):
        self.dots = set()
        for coord in coords:
            x, y = coord.split(",")
            self.dots.add((int(x), int(y)))
        self.folds = []
        for fold in folds:
            fold_core = fold.split()[-1]
            direction, value = fold_core.split("=")
            self.folds.append((direction, int(value)))

    def __str__(self):
        max_x = max(dot[0] for dot in self.dots)
        max_y = max(dot[1] for dot in self.dots)
        lines = ""
        for y in range(max_y + 1):
            for x in range(max_x + 1):
                lines += "#" if (x, y) in self.dots else "."
            lines += "\n"
        return lines

    def fold(self):
        new_dots = set()
        direction, value = self.folds.pop(0)
        for dot in self.dots:
            if (direction == "x" and dot[0] < value) or (
                direction != "x" and dot[1] < value
            ):
                new_dots.add(dot)
            elif direction == "x":
                new_dots.add((2 * value - dot[0], dot[1]))
            else:
                new_dots.add((dot[0], 2 * value - dot[1]))
        self.dots = new_dots

    def fold_all(self):
        while len(self.folds) > 0:
            self.fold()


def separate_coords_and_folds(lines):
    coords = []
    folds = []
    at_coords = True
    for line in lines:
        if not line.strip():
            at_coords = False
            continue
        if at_coords:
            coords.append(line)
        else:
            folds.append(line)

    return coords, folds


if __name__ == "__main__":
    paper = Paper(*separate_coords_and_folds(load_strs("inputs/day13.txt")))
    paper.fold()
    print(f"Part 1: {len(paper.dots)}")
    paper.fold_all()
    print("Part 2:")
    print(paper)


# -- Tests --
fixture = [
    "6,10",
    "0,14",
    "9,10",
    "0,3",
    "10,4",
    "4,11",
    "6,0",
    "6,12",
    "4,1",
    "0,13",
    "10,12",
    "3,4",
    "3,0",
    "8,4",
    "1,10",
    "2,14",
    "8,10",
    "9,0",
    "",
    "fold along y=7",
    "fold along x=5",
]


def test_separate_coords_and_folds():
    coords, folds = separate_coords_and_folds(fixture)
    assert len(coords) == 18
    assert len(folds) == 2


def test_part_1():
    coords, folds = separate_coords_and_folds(fixture)
    paper = Paper(coords, folds)
    paper.fold()
    assert len(paper.dots) == 17


def test_fold_all():
    paper = Paper(*separate_coords_and_folds(fixture))
    paper.fold_all()
    assert len(paper.dots) == 16


def test_str_does_not_blow_up():
    paper = Paper(*separate_coords_and_folds(fixture))
    paper.fold_all()
    paper = str(paper)
    assert paper[0] == "#"
