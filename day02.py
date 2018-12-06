#!/usr/bin/env python3
""" Part 01
"""

import os
import collections
import argparse


def part1(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    tags = inpt.strip().split('\n')
    tracker = collections.defaultdict(int)
    for tag in tags:
        count = collections.defaultdict(int)
        for i in tag:
            count[i] += 1
        if 2 in count.values():
            tracker[2] += 1
        if 3 in count.values():
            tracker[3] += 1
    return tracker[2] * tracker[3]


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    tags = inpt.strip().split('\n')
    length = len(tags[0])
    # pylint: disable=consider-using-enumerate
    for i in range(len(tags)):
        for j in range(len(tags)):
            if i == j:
                continue
            sum1 = [ord(tags[i][k]) for k in range(length)]
            sum2 = [ord(tags[j][k]) for k in range(length)]
            diff = [sum1[k] - sum2[k] for k in range(length)]
            subtract = [k for k in diff if k != 0]
            if len(subtract) == 1:
                index = diff.index(subtract[0])
                return ''.join([tags[i][k] for k in range(length) if k != index])
    return "You fucked up."


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
