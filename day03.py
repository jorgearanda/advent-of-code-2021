from loader import load_strs


def gamma(readings):
    counts = [0] * len(readings[0])
    for reading in readings:
        for idx, bit in enumerate(reading):
            counts[idx] += int(bit)
    gamma_bin = "".join("1" if count >= len(readings) / 2 else "0" for count in counts)
    return int(gamma_bin, 2)


def epsilon(readings):
    max_reading = 2 ** len(readings[0]) - 1
    return max_reading - gamma(readings)


def power(readings):
    return gamma(readings) * epsilon(readings)


def binary(val, length):
    return bin(val)[2:].rjust(length, "0")


def filter(readings, method):
    for idx in range(len(readings[0])):
        criterion = binary(method(readings), len(readings[0]))
        valid_readings = [r for r in readings if r[idx] == criterion[idx]]
        if len(valid_readings) == 1:
            break
        readings = valid_readings
    return int(valid_readings[0], 2)


def oxygen(readings):
    return filter(readings, gamma)


def co2(readings):
    return filter(readings, epsilon)


def life_support(readings):
    return oxygen(readings) * co2(readings)


if __name__ == "__main__":
    readings = load_strs("inputs/day03.txt")
    print(f"Part 1: {power(readings)}")
    print(f"Part 2: {life_support(readings)}")


# -- Tests --
fixture = [
    "00100",
    "11110",
    "10110",
    "10111",
    "10101",
    "01111",
    "00111",
    "11100",
    "10000",
    "11001",
    "00010",
    "01010",
]


def test_part_1():
    assert power(fixture) == 198


def test_binary():
    assert binary(gamma(fixture), 5) == "10110"
    assert binary(epsilon(fixture), 5) == "01001"


def test_oxygen():
    assert oxygen(fixture) == 23


def test_co2():
    assert co2(fixture) == 10


def test_part_2():
    assert life_support(fixture) == 230
