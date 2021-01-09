import threading
from typing import Callable, Dict

from util import read_input_as_lines


class Console(threading.Thread):
    def __init__(self, memory):
        super().__init__()
        self.memory = memory
        self.accumulator = 0
        self.instructions_run = list()
        self.instruction_pointer = 0
        self.inst_map: Dict[str, Callable[[int], None]] = {
            'acc': self.acc,
            'jmp': self.jmp,
            'nop': self.nop
        }

    def acc(self, param: int):
        self.accumulator += param

    def jmp(self, param: int):
        self.instruction_pointer += param

    def nop(self, param: int):
        pass

    def execute_instruction(self):
        instruction, param = self.memory[self.instruction_pointer].split(' ')
        inst_ptr_before = self.instruction_pointer
        self.inst_map[instruction](int(param))
        if self.instruction_pointer == inst_ptr_before:
            self.instruction_pointer += 1

    def run(self):
        while self.instruction_pointer not in self.instructions_run and self.instruction_pointer < len(self.memory):
            self.instructions_run.append(self.instruction_pointer)
            self.execute_instruction()


def part1():
    console = Console(read_input_as_lines())
    console.start()
    console.join()
    return console.accumulator


def part2():
    initial_memory = read_input_as_lines()
    memory = initial_memory
    tried_changing = set()
    while True:
        console = Console(memory)
        console.start()
        console.join()
        if console.instruction_pointer >= len(console.memory):
            return console.accumulator
        new_memory = initial_memory[:]
        # Try changing instructions, most recent ones first
        i_to_change = next(i for i in reversed(console.instructions_run)
                           if i not in tried_changing and
                           ('jmp' in new_memory[i] or 'nop' in new_memory[i]))
        tried_changing.add(i_to_change)
        new_memory[i_to_change] = \
            new_memory[i_to_change].replace('jmp', 'nop') \
                if 'jmp' in new_memory[i_to_change] else \
                new_memory[i_to_change].replace('nop', 'jmp')
        memory = new_memory


if __name__ == '__main__':
    print(part1())
    print(part2())
