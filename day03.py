#!/usr/bin/env python3
""" Part 01
"""

import os
import re
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
    result = set()
    for claim in claims:
        for i in range(claim.y_len):
            for j in range(max_x * claim.y_offset + i * max_x + claim.x_offset + 1,
                           claim.x_len + max_x * claim.y_offset + i * max_x + claim.x_offset + 1):
                fabric[j] += 1
                if fabric[j] > 1:
                    result.update([j])
    return len(result)


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    fabric = collections.defaultdict(list)
    max_x, max_y = 0, 0
    claim = collections.namedtuple('Claim', 'id x_offset y_offset x_len y_len')
    claims = []
    ids = set()
    for line in inpt.strip().split('\n'):
        tokens = re.search(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)', line).groups()
        newclaim = claim(int(tokens[0]), int(tokens[1]), int(tokens[2]), int(tokens[3]), int(tokens[4]))
        claims.append(newclaim)
        max_x = max(newclaim.x_offset + newclaim.x_len, max_x)
        max_y = max(newclaim.y_offset + newclaim.y_len, max_y)
        ids.update([newclaim.id])
    for claim in claims:
        for i in range(claim.y_len):
            for j in range(max_x * claim.y_offset + i * max_x + claim.x_offset + 1,
                           claim.x_len + max_x * claim.y_offset + i * max_x + claim.x_offset + 1):
                fabric[j].append(claim.id)
                if len(fabric[j]) > 1:
                    ids -= set(fabric[j])
    if len(ids) > 1:
        print(ids, len(ids))
        return "You fucked up."
    return list(ids)[0]


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
