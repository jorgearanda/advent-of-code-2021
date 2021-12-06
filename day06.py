from loader import load_comma_ints


def school_size(fish, days):
    ages = fish_ages(fish)
    for _ in range(days):
        ages = tick(ages)
    return sum(ages.values())


def fish_ages(fish):
    ages = {idx: 0 for idx in range(9)}
    for f in fish:
        ages[f] += 1
    return ages


def tick(ages):
    new_ages = {i: ages[i + 1] for i in range(8)}
    new_ages[6] += ages[0]
    new_ages[8] = ages[0]
    return new_ages


if __name__ == "__main__":
    fish = load_comma_ints("inputs/day06.txt")
    print(f"Part 1: {school_size(fish, days=80)}")
    print(f"Part 2: {school_size(fish, days=256)}")


# -- Tests --
fixture = [3, 4, 3, 1, 2]


def test_ages():
    assert fish_ages(fixture) == {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        4: 1,
        5: 0,
        6: 0,
        7: 0,
        8: 0,
    }


def test_part_1():
    assert school_size(fixture, days=80) == 5934


def test_part_2():
    assert school_size(fixture, days=256) == 26984457539
