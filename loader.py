def load_ints(filename):
    with open(filename) as f:
        return [int(line) for line in f.readlines()]


def load_strs(filename):
    with open(filename) as f:
        return [line.strip() for line in f.readlines()]


# -- Tests --
def test_load_ints():
    ints = load_ints("fixtures/ints.txt")
    assert ints == [123, 456, 789]


def test_load_strs():
    strs = load_strs("fixtures/strs.txt")
    assert strs == ["abc", "def", "ghi"]  # No newline
