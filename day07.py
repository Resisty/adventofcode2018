#!/usr/bin/env python3
""" Part 01
"""

import os
import re
import collections
import argparse
import pprint


class Node:
    """ Node class for DAG
    """
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.before = []
        self.after = []
    def __hash__(self):
        return hash(self.__dict__.values())
    def __eq__(self, other):
        return self.name == other.name
    def __lt__(self, other):
        return self.name < other.name
    def __str__(self):
        return f'{self.name}\n{", ".join([i.name for i in self.before])}\n{", ".join([i.name for i in self.after])}'

class KeyDefaultdict(collections.defaultdict):
    """ Default dict where KeyDefaultdict(C)[x] = C(x)
    """
    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        else:
            # pylint: disable=not-callable
            ret = self[key] = self.default_factory(key)
            return ret

def part1(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    nodes = KeyDefaultdict(Node)
    for line in inpt.strip().split('\n'):
        grps = re.search(r'Step (\w+) must be finished before step (\w+) can begin.', line)
        bfr, aftr = grps.groups()
        nodes[bfr].after = list(set(sorted(nodes[bfr].after + [nodes[aftr]])))
        #print(f'nodes[{bfr}].after: {[i.name for i in nodes[bfr].after]}')
        nodes[aftr].before = list(set(sorted(nodes[aftr].before + [nodes[bfr]])))
        #print(f'nodes[{aftr}].before: {[i.name for i in nodes[aftr].before]}')
    queue = sorted([node for name, node in nodes.items() if not node.before])
    print('Nodes without prior tasks:')
    print([i.name for i in queue])
    node = queue.pop(0)
    node.visited = True
    answer = node.name
    print(f'Selected node {answer} because it is first alphabetically.')
    queue = sorted(list(set(queue + node.after)))
    print(f"Adding {answer[-1]}'s next hops to the queue:")
    print([i.name for i in queue])
    while queue:
        for i in queue:
            if any([not j.visited for j in i.before]):
                print(f"Removing {i.name} from queue because dependent tasks have not been visited yet")
                print(f"{i.name}'s dependent tasks: {[j.name for j in i.before]}")
                queue.remove(i)
        print('Remaining available in queue:')
        print([i.name for i in queue])
        node = queue.pop(0)
        print(f'Selected node {node.name} because it is first alphabetically.')
        if node.visited:
            print(f'Node {node.name} has already been visited. Skipping.')
            continue
        node.visited = True
        answer += node.name
        print(f"Answer becomes: {answer}")
        queue = sorted(list(set(queue + node.after)))
        print('Updating queue:')
        print([i.name for i in queue])
    for i in nodes:
        assert i in answer
    return answer


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    return "not done yet"


def validate_and_open(path):
    """ Get the input file
    """
    if os.path.isfile(path):
        with open(path, 'r') as data:
            inpt = data.read()
        return inpt
    raise RuntimeError(f'Could not validate that {path} was a file for reading.')


if __name__ == '__main__':
    PARSER = argparse.ArgumentParser()
    PARSER.add_argument('input',
                        help='Path to input file')
    SUBS = PARSER.add_subparsers(dest='subparser_name')

    PART01 = SUBS.add_parser('1')
    PART01.set_defaults(func=part1)

    PART02 = SUBS.add_parser('2')
    PART02.set_defaults(func=part2)

    ARGS = PARSER.parse_args()
    print(ARGS.func(ARGS))
