from loader import load_strs


def max_height(y):
    return sum(range(1, abs(y[0])))


def x_bounds(x):
    x_max = x[1]
    for i in range(x[0] // 2, 1, -1):
        if sum(range(1, i + 1)) >= x[0]:
            x_min = i
    return (x_min, x_max)


def y_bounds(y):
    y_min = y[0]
    y_max = abs(y[0]) - 1
    return (y_min, y_max)


def throw(velocity, target):
    x_vel = velocity[0]
    y_vel = velocity[1]
    x_pos = y_pos = 0
    while x_pos <= target[0][1] and y_pos >= target[1][0]:
        x_pos += x_vel
        y_pos += y_vel
        x_vel = max(x_vel - 1, 0)
        y_vel -= 1
        if (
            target[0][0] <= x_pos <= target[0][1]
            and target[1][0] <= y_pos <= target[1][1]
        ):
            return True
    return False


def find_throws(target):
    x_vel_bounds = x_bounds(target[0])
    y_vel_bounds = y_bounds(target[1])
    on_target = 0
    for i in range(x_vel_bounds[0], x_vel_bounds[1] + 1):
        for j in range(y_vel_bounds[0], y_vel_bounds[1] + 1):
            if throw((i, j), target):
                on_target += 1
    return on_target


def parse_input(line):
    x_str, y_str = line[13:].split(", ")
    x_min, x_max = x_str[2:].split("..")
    y_min, y_max = y_str[2:].split("..")
    return (int(x_min), int(x_max)), (int(y_min), int(y_max))


if __name__ == "__main__":
    target = parse_input(load_strs("inputs/day17.txt")[0])
    print(f"Part 1: {max_height(target[1])}")
    print(f"Part 2: {find_throws(target)}")


# -- Tests --
def test_part_1():
    _, y = parse_input("target area: x=20..30, y=-10..-5")
    assert max_height(y) == 45


def test_x_bounds():
    assert x_bounds((20, 30)) == (6, 30)


def test_y_bounds():
    assert y_bounds((-10, -5)) == (-10, 9)


def test_part_2():
    target = parse_input("target area: x=20..30, y=-10..-5")
    assert find_throws(target) == 112
