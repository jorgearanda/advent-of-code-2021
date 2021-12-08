from loader import load_strs


class Entry:
    def __init__(self, line):
        signal_patterns_str, output_str = line.split(" | ")
        self.signals = [set(signal) for signal in signal_patterns_str.split()]
        self.output = [set(output) for output in output_str.split()]
        self.mapping = {}
        self.deduce()
        self.output_value = self.map_output()

    def deduce(self):
        self.find_uniques()
        self.find_3()
        self.find_9()
        self.find_5()
        self.find_2()
        self.find_0()
        self.find_6()

    def find_uniques(self):
        for signal in self.signals:
            match len(signal):
                case 2:
                    self.mapping[1] = signal
                case 3:
                    self.mapping[7] = signal
                case 4:
                    self.mapping[4] = signal
                case 7:
                    self.mapping[8] = signal
                case _:
                    continue

    def find_3(self):
        for signal in self.signals:
            if len(signal) == 5 and signal.issuperset(self.mapping[7]):
                self.mapping[3] = signal
                break

    def find_9(self):
        for signal in self.signals:
            if len(signal) == 6 and signal.issuperset(self.mapping[3]):
                self.mapping[9] = signal
                break

    def find_5(self):
        for signal in self.signals:
            if (
                len(signal) == 5
                and signal != self.mapping[3]
                and signal.issubset(self.mapping[9])
            ):
                self.mapping[5] = signal
                break

    def find_2(self):
        for signal in self.signals:
            if (
                len(signal) == 5
                and signal != self.mapping[3]
                and signal != self.mapping[5]
            ):
                self.mapping[2] = signal
                break

    def find_0(self):
        for signal in self.signals:
            if (
                len(signal) == 6
                and signal != self.mapping[9]
                and signal.issuperset(self.mapping[1])
            ):
                self.mapping[0] = signal
                break

    def find_6(self):
        for signal in self.signals:
            if (
                len(signal) == 6
                and signal != self.mapping[9]
                and signal != self.mapping[0]
            ):
                self.mapping[6] = signal
                break

    def map_output(self):
        total = 0
        for val, signal in self.mapping.items():
            if self.output[0] == signal:
                total += val * 1_000
            if self.output[1] == signal:
                total += val * 100
            if self.output[2] == signal:
                total += val * 10
            if self.output[3] == signal:
                total += val * 1
        return total


def count_unique_lengths(entries):
    res = 0
    for entry in entries:
        for output in entry.output:
            if len(output) in {2, 3, 4, 7}:
                res += 1
    return res


def parse_input(lines):
    return [Entry(line) for line in lines]


if __name__ == "__main__":
    entries = parse_input(load_strs("inputs/day08.txt"))
    print(f"Part 1: {count_unique_lengths(entries)}")
    print(f"Part 2: {sum(entry.output_value for entry in entries)}")


# -- Tests --
fixture = load_strs("fixtures/seven_segment_display.txt")


def test_part_1():
    assert count_unique_lengths(parse_input(fixture)) == 26


def test_part_2():
    assert sum(entry.output_value for entry in parse_input(fixture)) == 61229
