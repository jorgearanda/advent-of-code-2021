from dataclasses import dataclass

from loader import load_strs


class Board:
    def __init__(self, board_rows):
        self.cells = []
        for row in board_rows:
            self.cells.append([Cell(int(number), False) for number in row.split()])
        self.transposed = list(map(list, zip(*self.cells)))
        self.last_called = None

    def call(self, number):
        self.last_called = number
        for row in self.cells:
            for cell in row:
                if cell.value == number:
                    cell.called = True

    def is_winner(self):
        for row in self.cells:
            if all(cell.called for cell in row):
                return True
        for row in self.transposed:
            if all(cell.called for cell in row):
                return True
        return False

    def score(self):
        return (
            sum(cell.value for row in self.cells for cell in row if not cell.called)
            * self.last_called
        )


@dataclass
class Cell:
    value: int
    called: bool


def parse_input(lines):
    draw = [int(val) for val in lines[0].split(",")]
    boards = []
    board_lines = []
    for line in lines[2:]:
        if line == "":
            boards.append(Board(board_lines))
            board_lines = []
        else:
            board_lines.append(line)
    if len(board_lines) > 0:
        boards.append(Board(board_lines))

    return draw, boards


def play(draw, boards, to_win=True):
    winning_boards = set()
    for num in draw:
        for board in boards:
            board.call(num)
            if board.is_winner():
                winning_boards.add(board)
                if to_win:
                    return board.score()
                elif len(winning_boards) == len(boards):
                    return board.score()


if __name__ == "__main__":
    print(f"Part 1: {play(*parse_input(load_strs('inputs/day04.txt')))}")
    print(f"Part 2: {play(*parse_input(load_strs('inputs/day04.txt')), to_win=False)}")


# -- Tests --
fixture = load_strs("fixtures/bingo.txt")


def test_board_initializes():
    b = Board(["1 2 3", "4 5 6", "7 8 9"])
    assert b


def test_board_winner_row():
    b = Board(["1 2 3", "4 5 6", "7 8 9"])
    assert not b.is_winner()
    b.call(5)
    assert not b.is_winner()
    b.call(6)
    assert not b.is_winner()
    b.call(4)
    assert b.is_winner()


def test_board_winner_col():
    b = Board(["1 2 3", "4 5 6", "7 8 9"])
    assert not b.is_winner()
    b.call(5)
    assert not b.is_winner()
    b.call(2)
    assert not b.is_winner()
    b.call(8)
    assert b.is_winner()


def test_parse_input():
    draw, boards = parse_input(fixture)
    assert len(draw) == 27
    assert len(boards) == 3
    assert boards[0].cells[0][0].value == 22
    assert boards[2].cells[4][4].value == 7


def test_part_1():
    assert play(*parse_input(fixture)) == 4512


def test_part_2():
    assert play(*parse_input(fixture), to_win=False) == 1924
