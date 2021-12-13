from loader import load_strs


class Octomap:
    def __init__(self, lines):
        self.cells = [
            [Octopus(i, j, cell, self) for i, cell in enumerate(line)]
            for j, line in enumerate(lines)
        ]
        for row in self.cells:
            for octopus in row:
                octopus.scout()
        self.curr_step = 0
        self.all_burst = None

    def __str__(self):
        return "".join(
            f"{''.join(str(octopus.level) for octopus in row)}\n" for row in self.cells
        )

    def steps(self, num):
        for _ in range(num):
            self.step()

    def steps_until_all_burst(self):
        while self.all_burst is None:
            self.step()
        return self.all_burst

    def step(self):
        self.curr_step += 1
        for row in self.cells:
            for octopus in row:
                octopus.increase_level()
        while any(
            octopus.level > 9 and not octopus.burst
            for row in self.cells
            for octopus in row
        ):
            for row in self.cells:
                for octopus in row:
                    if octopus.level > 9 and not octopus.burst:
                        octopus.spread_burst()
        if all(octopus.burst for row in self.cells for octopus in row):
            self.all_burst = self.curr_step
        for row in self.cells:
            for octopus in row:
                octopus.wipe_level()

    def bursts(self):
        return sum(octopus.bursts for row in self.cells for octopus in row)


class Octopus:
    def __init__(self, x, y, level, octomap):
        self.x = x
        self.y = y
        self.level = int(level)
        self.octomap = octomap
        self.neighbours = None
        self.burst = False
        self.bursts = 0

    def scout(self):
        self.calc_neighbours()

    def calc_neighbours(self):
        self.top_edge = self.y == 0
        self.bottom_edge = self.y == len(self.octomap.cells) - 1
        self.left_edge = self.x == 0
        self.right_edge = self.x == len(self.octomap.cells[self.y]) - 1
        self.neighbours = []

        # Left column
        if not self.left_edge:
            self.neighbours.append(self.octomap.cells[self.y][self.x - 1])
            if not self.top_edge:
                self.neighbours.append(self.octomap.cells[self.y - 1][self.x - 1])
            if not self.bottom_edge:
                self.neighbours.append(self.octomap.cells[self.y + 1][self.x - 1])

        # Middle column
        if not self.top_edge:
            self.neighbours.append(self.octomap.cells[self.y - 1][self.x])
        if not self.bottom_edge:
            self.neighbours.append(self.octomap.cells[self.y + 1][self.x])

        # Right column
        if not self.right_edge:
            self.neighbours.append(self.octomap.cells[self.y][self.x + 1])
            if not self.top_edge:
                self.neighbours.append(self.octomap.cells[self.y - 1][self.x + 1])
            if not self.bottom_edge:
                self.neighbours.append(self.octomap.cells[self.y + 1][self.x + 1])

    def increase_level(self):
        self.level += 1

    def spread_burst(self):
        self.bursts += 1
        self.burst = True
        for neighbour in self.neighbours:
            neighbour.increase_level()

    def wipe_level(self):
        if self.level > 9:
            self.level = 0
            self.burst = False


if __name__ == "__main__":
    octomap = Octomap(load_strs("inputs/day11.txt"))
    octomap.steps(100)
    print(f"Part 1: {octomap.bursts()}")
    print(f"Part 2: {octomap.steps_until_all_burst()}")


# -- Tests --
fixture = [
    "5483143223",
    "2745854711",
    "5264556173",
    "6141336146",
    "6357385478",
    "4167524645",
    "2176841721",
    "6882881134",
    "4846848554",
    "5283751526",
]


def test_neighbours():
    octomap = Octomap(fixture)
    assert len(octomap.cells) == 10
    assert len(octomap.cells[0][0].neighbours) == 3
    assert len(octomap.cells[5][5].neighbours) == 8
    assert len(octomap.cells[9][9].neighbours) == 3


def test_part_1():
    octomap = Octomap(fixture)
    octomap.steps(100)
    assert octomap.bursts() == 1656


def test_part_2():
    octomap = Octomap(fixture)
    assert octomap.steps_until_all_burst() == 195
