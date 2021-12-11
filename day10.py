from statistics import median

from loader import load_strs


corrupt_map = {
    ")": 3,
    "]": 57,
    "}": 1197,
    ">": 25137,
}

expected_closer = {
    "[": "]",
    "(": ")",
    "{": "}",
    "<": ">",
}

autocomplete_map = {
    "(": 1,
    "[": 2,
    "{": 3,
    "<": 4,
}


def corrupt_score(line):
    stack = []
    close_chars = set("])}>")
    expected = None
    for char in line:
        if expected and char in close_chars and expected != char:
            return corrupt_map[char]
        if char in close_chars:
            stack.pop()
            expected = None if not stack else expected_closer[stack[-1]]
        else:
            stack.append(char)
            expected = expected_closer[char]
    return 0


def total_corrupt_score(lines):
    return sum(corrupt_score(line) for line in lines)


def autocomplete_score(line):
    if corrupt_score(line) != 0:
        return 0
    stack = []
    close_chars = set("])}>")
    for char in line:
        if char in close_chars:
            stack.pop()
        else:
            stack.append(char)

    score = 0
    for char in stack[::-1]:
        score *= 5
        score += autocomplete_map[char]
    return score


def total_autocomplete_score(lines):
    scores = [autocomplete_score(line) for line in lines]
    scores = [score for score in scores if score > 0]
    return median(scores)


if __name__ == "__main__":
    lines = load_strs("inputs/day10.txt")
    print(f"Part 1: {total_corrupt_score(lines)}")
    print(f"Part 2: {total_autocomplete_score(lines)}")


# -- Tests --
fixture = [
    "[({(<(())[]>[[{[]{<()<>>",
    "[(()[<>])]({[<{<<[]>>(",
    "{([(<{}[<>[]}>{[]{[(<()>",
    "(((({<>}<{<{<>}{[]{[]{}",
    "[[<[([]))<([[{}[[()]]]",
    "[{[{({}]{}}([{[{{{}}([]",
    "{<[[]]>}<{[{[{[]{()[[[]",
    "[<(<(<(<{}))><([]([]()",
    "<{([([[(<>()){}]>(<<{{",
    "<{([{{}}[<[[[<>{}]]]>[]]",
]


def test_part_1():
    assert total_corrupt_score(fixture) == 26397


def test_part_2():
    assert total_autocomplete_score(fixture) == 288957
