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
    total = 0
    joined = ''.join([i.strip() for i in inpt.strip().split('\n')])
    parts = re.findall(r'(([-+]+)(\d+))', joined)
    for threepart in parts:
        sign = threepart[1]
        num = threepart[2]
        for bit in sign:
            num = 0 - int(num) if bit == '-' else int(num)
        total += num
        print(f'Adding {num} to total: {total}')
    return total


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    total = 0
    totals = collections.defaultdict(int)
    joined = ''.join([i.strip() for i in inpt.strip().split('\n')])
    while True:
        parts = re.findall(r'(([-+]+)(\d+))', joined)
        for threepart in parts:
            sign = threepart[1]
            num = threepart[2]
            for bit in sign:
                num = 0 - int(num) if bit == '-' else int(num)
            total += num
            totals[total] += 1
            if totals[total] > 1:
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
    print(ARGS.func(ARGS))
