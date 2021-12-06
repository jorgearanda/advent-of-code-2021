def load_ints(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def load_comma_ints(filename):
    with open(filename) as f:
        return [int(token) for token in f.read().split(",")]


def load_strs(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


# -- Tests --
def test_load_ints():
    ints = load_ints("fixtures/ints.txt")
    assert ints == [123, 456, 789]


def test_load_comma_ints():
    ints = load_comma_ints("fixtures/comma_ints.txt")
    assert ints == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_load_strs():
    strs = load_strs("fixtures/strs.txt")
    assert strs == ["abc", "def", "ghi"]  # No newline
