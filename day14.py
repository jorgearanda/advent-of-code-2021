from loader import load_strs


def prepare_pairs(template):
    pairs = {}
    for i in range(len(template) - 1):
        pair = template[i : i + 2]
        pairs.setdefault(pair, 0)
        pairs[pair] += 1
    return pairs


def step(pairs, rules):
    new_pairs = {}
    for pair, amount in pairs.items():
        left = pair[0] + rules[pair]
        right = rules[pair] + pair[1]
        new_pairs.setdefault(left, 0)
        new_pairs[left] += amount
        new_pairs.setdefault(right, 0)
        new_pairs[right] += amount
    return new_pairs


def count_elements(template, rules, steps):
    pairs = prepare_pairs(template)
    for _ in range(steps):
        pairs = step(pairs, rules)

    counts = {}
    for pair, amount in pairs.items():
        counts.setdefault(pair[0], 0)
        counts[pair[0]] += amount

    counts.setdefault(template[-1], 0)
    counts[template[-1]] += 1

    return counts


def max_to_min(counts):
    return max(counts.values()) - min(counts.values())


def parse_input(lines):
    template = lines[0]
    rules = {}
    for line in lines[2:]:
        pair, insertion = line.split(" -> ")
        rules[pair] = insertion
    return template, rules


if __name__ == "__main__":
    lines = load_strs("inputs/day14.txt")
    counts = count_elements(*parse_input(lines), steps=10)
    print(f"Part 1: {max_to_min(counts)}")
    counts = count_elements(*parse_input(lines), steps=40)
    print(f"Part 2: {max_to_min(counts)}")


# -- Tests --
fixture = [
    "NNCB",
    "",
    "CH -> B",
    "HH -> N",
    "CB -> H",
    "NH -> C",
    "HB -> C",
    "HC -> B",
    "HN -> C",
    "NN -> C",
    "BH -> H",
    "NC -> B",
    "NB -> B",
    "BN -> B",
    "BB -> N",
    "BC -> B",
    "CC -> N",
    "CN -> C",
]


def test_parse_input():
    template, rules = parse_input(fixture)
    assert template == "NNCB"
    assert rules["BN"] == "B"


def test_prepare_pairs():
    template, _ = parse_input(fixture)
    pairs = prepare_pairs(template)
    assert len(pairs) == 3
    assert pairs["NC"] == 1


def test_count_elements():
    counts = count_elements(*parse_input(fixture), steps=0)
    assert counts["N"] == 2
    assert counts["C"] == 1


def test_part_1():
    counts = count_elements(*parse_input(fixture), steps=10)
    assert max_to_min(counts) == 1588


def test_part_2():
    counts = count_elements(*parse_input(fixture), steps=40)
    assert max_to_min(counts) == 2188189693529
