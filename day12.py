from loader import load_strs


class CaveSystem:
    def __init__(self, connections):
        self.caves = {}
        for conn in connections:
            cave1, cave2 = conn.split("-")
            self.caves.setdefault(cave1, [])
            self.caves[cave1].append(cave2)
            self.caves.setdefault(cave2, [])
            self.caves[cave2].append(cave1)


def find_paths(cave_system, from_cave, cur_path, allow_repeat=False):
    if len(cur_path) > 0:
        cur_path += "," + from_cave
    else:
        cur_path = from_cave
    if from_cave == "end":
        return [cur_path]
    paths = []
    for cave in cave_system.caves[from_cave]:
        if (
            cave.isupper()
            or cave not in cur_path
            or (
                allow_repeat
                and cave not in {"start", "end"}
                and not has_repeat(cur_path)
            )
        ):
            paths.extend(find_paths(cave_system, cave, cur_path, allow_repeat))
    return paths


def has_repeat(path):
    small_caves = [cave for cave in path.split(",") if cave.islower()]
    return len(small_caves) > len(set(small_caves))


if __name__ == "__main__":
    cs = CaveSystem(load_strs("inputs/day12.txt"))
    print(f"Part 1: {len(find_paths(cs, 'start', ''))}")
    print(f"Part 2: {len(find_paths(cs, 'start', '', True))}")


# -- Tests --
simple_system = [
    "start-A",
    "start-b",
    "A-c",
    "A-b",
    "b-d",
    "A-end",
    "b-end",
]


def test_part_1():
    assert len(find_paths(CaveSystem(simple_system), "start", "")) == 10


def test_part_2():
    assert len(find_paths(CaveSystem(simple_system), "start", "", True)) == 36
