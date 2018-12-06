#!/usr/bin/env python3
""" Part 01
"""

import os
import re
import pprint
import collections
import argparse


def part1(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    fabric = collections.defaultdict(int)
    max_x, max_y = 0, 0
    claim = collections.namedtuple('Claim', 'x_offset y_offset x_len y_len')
    claims = []
    for line in inpt.strip().split('\n'):
        tokens = re.search(r'#\d+ @ (\d+),(\d+): (\d+)x(\d+)', line).groups()
        claims.append(claim(int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3])))
        max_x = max(claims[-1].x_offset + claims[-1].x_len, max_x)
        max_y = max(claims[-1].y_offset + claims[-1].y_len, max_y)
    print(f'Total spots: {max_x * max_y}')
    for claim in claims:
        for i in range(claim.y_len):
            for j in range(max_x * claim.y_offset + i * max_x + claim.x_offset + 1,
                           claim.x_len + max_x * claim.y_offset + i * max_x + claim.x_offset + 1):
                fabric[j] += 1
    return len([i for i, j in fabric.items() if j > 1])


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    return "Not implemented"


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
