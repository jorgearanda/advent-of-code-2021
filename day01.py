from loader import load_ints


def increases(vals, offset=1):
    return sum(a < b for a, b in zip(vals, vals[offset:]))


if __name__ == "__main__":
    vals = load_ints("inputs/day01.txt")
    print(f"Part 1: {increases(vals)}")
    print(f"Part 2: {increases(vals, offset=3)}")


# -- Tests --
fixture = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]


def test_part_1():
    assert increases(fixture) == 7


def test_part_2():
    assert increases(fixture, offset=3) == 5
