from loader import load_ints


def increases(vals):
    return sum(a < b for a, b in zip(vals, vals[1:]))


def windows(vals):
    return [sum(items) for items in zip(vals, vals[1:], vals[2:])]


if __name__ == "__main__":
    vals = load_ints("inputs/day01.txt")
    print(f"Part 1: {increases(vals)}")
    print(f"Part 2: {increases(windows(vals))}")


# -- Tests --
fixture = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_part_1():
    assert increases(fixture) == 7


def test_part_2():
    assert increases(windows(fixture)) == 5
