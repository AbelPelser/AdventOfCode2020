puzzle_input = list(map(int, list('586439172')))


class LinkedList:
    def __init__(self):
        self.root = None
        self.current = None
        self.node_dict = {}

    def add_node(self, cup):
        new = Node(cup)
        self.node_dict[cup] = new
        if self.current:
            self.current.next = new
        new.prev = self.current
        self.current = new
        if not self.root:
            self.root = new

    def make_circular(self):
        self.current.next = self.root
        self.root.prev = self.current

    @staticmethod
    def remove_segment(after_node, n_nodes):
        if n_nodes == 0:
            return None
        start = end = after_node.next
        for i in range(n_nodes - 1):
            end = end.next
        start.prev.next = end.next
        end.next.prev = start.prev
        start.prev = None
        end.next = None
        return start, end

    @staticmethod
    def insert_segment(start, end, after_node):
        after_node.next.prev = end
        end.next = after_node.next
        after_node.next = start
        start.prev = after_node

    @staticmethod
    def to_str(start):
        output = str(start.cup)
        node = start.next
        while node != start:
            output += str(node.cup)
            node = node.next
        return output


class Node:
    def __init__(self, cup):
        self.prev = None
        self.next = None
        self.cup = cup


def make_cups_list(cups, length):
    linked_list = LinkedList()

    for cup in cups:
        linked_list.add_node(cup)
    for cup in range(max(cups) + 1, length + 1):
        linked_list.add_node(cup)
    linked_list.make_circular()
    linked_list.current = linked_list.root
    return linked_list


def play(starting_cups, total_n_cups, n_rounds):
    cups_list = make_cups_list(starting_cups, total_n_cups)

    for _ in range(n_rounds):
        pick_start, pick_end = LinkedList.remove_segment(cups_list.current, 3)
        cups_picked = [n.cup for n in [pick_start, pick_start.next, pick_end]]
        dest_val = (cups_list.current.cup - 1) % (total_n_cups + 1)
        while dest_val in cups_picked or dest_val == 0:
            dest_val = (dest_val - 1) % (total_n_cups + 1)
        LinkedList.insert_segment(pick_start, pick_end, cups_list.node_dict[dest_val])
        cups_list.current = cups_list.current.next
    return cups_list


def part1():
    return LinkedList.to_str(play(puzzle_input, len(puzzle_input), 100).node_dict[1])[1:]


def part2():
    node1 = play(puzzle_input, 1000000, 10000000).node_dict[1]
    return node1.next.cup * node1.next.next.cup


if __name__ == '__main__':
    print(part1())
    print(part2())
