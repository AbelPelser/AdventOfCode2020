import re

from util import read_input_as_lines


def apply_bm_to_val(bit_mask, val):
    return ''.join(val_bit if mask_bit == 'X' else mask_bit
                   for mask_bit, val_bit in zip(bit_mask, val))


def apply_bm_to_addr(bit_mask, addr):
    return ''.join([mask_bit if mask_bit == 'X' else str(int(val_bit) | int(mask_bit))
                    for mask_bit, val_bit in zip(bit_mask, addr)])


def write_to_memory_part1(memory, addr_bit_str, val_bit_str, bit_mask):
    memory[int(addr_bit_str, 2)] = int(apply_bm_to_val(bit_mask, val_bit_str), 2)


def write_to_memory_part2(memory, addr_bit_str, val_bit_str, bit_mask):
    addr_bit_str_floating = apply_bm_to_addr(bit_mask, addr_bit_str)
    for addr_bit_str_concrete in expand_float_addr(addr_bit_str_floating):
        memory[int(addr_bit_str_concrete, 2)] = int(val_bit_str, 2)


def expand_float_addr(addr):
    if 'X' not in addr:
        yield addr
    else:
        work_list = {addr}
        while len(work_list) > 0:
            addr = work_list.pop()
            new_addr0, new_addr1 = addr.replace('X', '0', 1), addr.replace('X', '1', 1)
            if 'X' in new_addr0:
                work_list.add(new_addr0)
                work_list.add(new_addr1)
            else:
                yield new_addr0
                yield new_addr1


def init_memory(lines, write_to_memory):
    memory = dict()
    bm = None
    for line in lines:
        if line.startswith('mask'):
            bm, = re.match('mask = ([01X]*)', line).groups()
        else:
            addr_str, val_str = re.match('mem\\[([0-9]*)] = ([0-9]*)', line).groups()
            val_bit_str = bin(int(val_str))[2:].rjust(len(bm), '0')
            addr_bit_str = bin(int(addr_str))[2:].rjust(len(bm), '0')
            write_to_memory(memory, addr_bit_str, val_bit_str, bm)
    return sum(memory.values())


def part1():
    return init_memory(read_input_as_lines(), write_to_memory_part1)


def part2():
    return init_memory(read_input_as_lines(), write_to_memory_part2)


if __name__ == '__main__':
    print(part1())
    print(part2())
