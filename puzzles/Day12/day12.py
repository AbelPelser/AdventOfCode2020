import math
from abc import ABC, abstractmethod

from util import read_input_as_lines


class NavigationComputer(ABC):
    def __init__(self):
        self.location = [0, 0]

    @abstractmethod
    def left(self, amount: int):
        pass

    @abstractmethod
    def right(self, amount: int):
        pass

    @abstractmethod
    def north(self, amount: int):
        pass

    @abstractmethod
    def south(self, amount: int):
        pass

    @abstractmethod
    def west(self, amount: int):
        pass

    @abstractmethod
    def east(self, amount: int):
        pass

    @abstractmethod
    def forward(self, amount: int):
        pass

    def run(self, input_lines):
        for line in input_lines:
            c = line[0]
            amount = int(line[1:])
            if c == 'L':
                self.left(amount)
            elif c == 'R':
                self.right(amount)
            elif c == 'N':
                self.north(amount)
            elif c == 'S':
                self.south(amount)
            elif c == 'E':
                self.east(amount)
            elif c == 'W':
                self.west(amount)
            elif c == 'F':
                self.forward(amount)
        return abs(self.location[0]) + abs(self.location[1])


class NavigationComputer1(NavigationComputer):
    def __init__(self):
        super().__init__()
        self.direction_i = 0
        # east, north, west, south
        self.direction_steps = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def left(self, amount: int):
        self.direction_i = int(self.direction_i + (amount / 90)) % len(self.direction_steps)

    def right(self, amount: int):
        self.direction_i = int(self.direction_i - (amount / 90)) % len(self.direction_steps)

    def north(self, amount: int):
        self.location[1] += amount

    def south(self, amount: int):
        self.location[1] -= amount

    def east(self, amount: int):
        self.location[0] += amount

    def west(self, amount: int):
        self.location[0] -= amount

    def forward(self, amount: int):
        d_x, d_y = self.direction_steps[self.direction_i]
        self.location[0] += d_x * amount
        self.location[1] += d_y * amount


class NavigationComputer2(NavigationComputer):
    def __init__(self):
        super().__init__()
        self.relative_waypoint = [10, 1]

    def rotate_waypoint(self, degrees):
        x, y = self.relative_waypoint
        radians = math.pi * 2 * degrees / 360
        new_x = round(x * math.cos(radians) + y * math.sin(radians))
        new_y = round(-x * math.sin(radians) + y * math.cos(radians))
        self.relative_waypoint = [new_x, new_y]

    def left(self, amount: int):
        self.rotate_waypoint(-amount)

    def right(self, amount: int):
        self.rotate_waypoint(amount)

    def north(self, amount: int):
        self.relative_waypoint[1] += amount

    def south(self, amount: int):
        self.relative_waypoint[1] -= amount

    def east(self, amount: int):
        self.relative_waypoint[0] += amount

    def west(self, amount: int):
        self.relative_waypoint[0] -= amount

    def forward(self, amount: int):
        self.location[0] += self.relative_waypoint[0] * amount
        self.location[1] += self.relative_waypoint[1] * amount


def part1():
    return NavigationComputer1().run(read_input_as_lines())


def part2():
    return NavigationComputer2().run(read_input_as_lines())


if __name__ == '__main__':
    print(part1())
    print(part2())
