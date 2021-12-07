from statistics import median

from loader import load_comma_ints


def min_fuel_simple(positions):
    optimal = median(positions)
    return int(sum(abs(position - optimal) for position in positions))


def fuel(target, positions):
    return int(sum(sum(range(abs(position - target) + 1)) for position in positions))


def min_fuel_increasing(positions):
    optimal_fuel = 1_000_000_000
    for target in range(min(positions), max(positions)):
        target_fuel = fuel(target, positions)
        if target_fuel > optimal_fuel:
            return optimal_fuel
        optimal_fuel = target_fuel


if __name__ == "__main__":
    positions = load_comma_ints("inputs/day07.txt")
    print(f"Part 1: {min_fuel_simple(positions)}")
    print(f"Part 2: {min_fuel_increasing(positions)}")


# -- Tests --
fixture = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]


def test_part_1():
    assert min_fuel_simple(fixture) == 37


def test_part_2():
    assert min_fuel_increasing(fixture) == 168
