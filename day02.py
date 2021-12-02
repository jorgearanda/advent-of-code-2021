from loader import load_strs


class Instruction:
    def __init__(self, line):
        tokens = line.split(" ")
        self.direction = tokens[0]
        self.magnitude = int(tokens[1])


class Submarine:
    def __init__(self, instructions):
        self.horizontal = 0
        self.depth = 0
        self.aim = 0
        for instruction in instructions:
            self.run(instruction)  # In subclasses

    def report(self):
        return self.depth * self.horizontal


class SubmarineType1(Submarine):
    def run(self, instruction):
        match instruction.direction:
            case "forward":
                self.horizontal += instruction.magnitude
            case "down":
                self.depth += instruction.magnitude
            case "up":
                self.depth -= instruction.magnitude


class SubmarineType2(Submarine):
    def run(self, instruction):
        match instruction.direction:
            case "forward":
                self.horizontal += instruction.magnitude
                self.depth += instruction.magnitude * self.aim
            case "down":
                self.aim += instruction.magnitude
            case "up":
                self.aim -= instruction.magnitude


def parse_input(lines):
    return [Instruction(line) for line in lines]


if __name__ == "__main__":
    instructions = parse_input(load_strs("inputs/day02.txt"))
    print(f"Part 1: {SubmarineType1(instructions).report()}")
    print(f"Part 2: {SubmarineType2(instructions).report()}")


# -- Tests --
fixture = [
    "forward 5",
    "down 5",
    "forward 8",
    "up 3",
    "down 8",
    "forward 2",
]


def test_part_1():
    assert SubmarineType1(parse_input(fixture)).report() == 150


def test_part_2():
    assert SubmarineType2(parse_input(fixture)).report() == 900
