#!/usr/bin/env python3
""" Part 01
"""

import os
import re
import collections
import argparse
import pprint
from queue import PriorityQueue, Empty

MAX_WORKERS = 5
DEFAULT_SECONDS = 60

class Node:
    """ Node class for DAG
    """
    def __init__(self, name):
        self.name = name
        self.visited = False
        self.seconds = ord(name) - ord('A') + DEFAULT_SECONDS + 1
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
        nodes[bfr].after = sorted(list(set(nodes[bfr].after + [nodes[aftr]])))
        nodes[aftr].before = sorted(list(set(nodes[aftr].before + [nodes[bfr]])))
    queue = PriorityQueue()
    for _, node in nodes.items():
        if not node.before:
            queue.put(node)
    print('Nodes without prior tasks:')
    print([i.name for i in queue.__dict__['queue']])
    node = queue.get()
    node.visited = True
    answer = node.name
    print(f'Selected node {answer} because it is first alphabetically.')
    for nextnode in node.after:
        queue.put(nextnode)
    print(f"Adding {answer[-1]}'s next hops to the queue:")
    print([i.name for i in queue.__dict__['queue']])
    while queue.not_empty:
        try:
            i = queue.get_nowait()
        except Empty:
            break
        print(f'Got node from front of queue: {i.name}')
        if any([not j.visited for j in i.before]):
            print(f"Removing {i.name} from queue because dependent tasks have not been visited yet")
            continue
        print(f'Selected node {i.name} because it is first alphabetically.')
        if i.visited:
            print(f'Already visited {i.name}, skipping.')
            continue
        i.visited = True
        answer += i.name
        print(f"Answer becomes: {answer}")
        for nextnode in i.after:
            if not nextnode.visited:
                queue.put(nextnode)
        print(f"Adding {answer[-1]}'s next hops to the queue:")
        print([j.name for j in queue.__dict__['queue']])
    for i in nodes:
        assert i in answer
    return answer


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    nodes = KeyDefaultdict(Node)
    for line in inpt.strip().split('\n'):
        grps = re.search(r'Step (\w+) must be finished before step (\w+) can begin.', line)
        bfr, aftr = grps.groups()
        nodes[bfr].after = sorted(list(set(nodes[bfr].after + [nodes[aftr]])))
        nodes[aftr].before = sorted(list(set(nodes[aftr].before + [nodes[bfr]])))
    queue = PriorityQueue()
    workers = []
    for _, node in nodes.items():
        if not node.before:
            queue.put(node)
    print('Nodes without prior tasks:')
    print([i.name for i in queue.__dict__['queue']])
    node = queue.get()
    total = 0
    answer = ''
    workers.append(node)
    print(f'Selected node {node.name} because it is first alphabetically.')
    while workers:
        shortest_work = min(workers, key=lambda x: x.seconds)
        elapsed = shortest_work.seconds
        print(f'Workers in the queue: {[i.name for i in workers]}')
        print(f'Worker {shortest_work.name} next to complete in {elapsed} seconds.')
        total += elapsed
        to_pop = []
        for worker in workers:
            worker.seconds -= elapsed
            print(f'Worker {worker.name} time left: {worker.seconds} seconds.')
            if worker.seconds == 0:
                worker.visited = True
                to_pop.append(worker)
                answer += worker.name
                for nextnode in worker.after:
                    if not nextnode.visited:
                        queue.put(nextnode)
                        print(f"Adding {worker.name}'s next hops to the queue:")
                        print([i.name for i in queue.__dict__['queue']])
        for pop_me in to_pop:
            workers.remove(pop_me)
        print(f'Some workers finished. Answer updated to {answer}')
        while len(workers) < MAX_WORKERS:
            try:
                i = queue.get_nowait()
            except Empty:
                break
            print(f'Got node from front of queue: {i.name}')
            if any([not j.visited for j in i.before]):
                print(f"Removing {i.name} from queue because dependent tasks have not been visited yet")
                continue
            print(f'Selected node {i.name} because it is first alphabetically.')
            if i.visited:
                print(f'Already visited {i.name}, skipping.')
                continue
            workers.append(i)
            print(f'Starting work on {i.name} for {i.seconds} seconds')
    return total


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
    if 'test' in ARGS.input:
        MAX_WORKERS = 2
        DEFAULT_SECONDS = 0
    print(ARGS.func(ARGS))
