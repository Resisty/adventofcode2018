#!/usr/bin/env python3
""" Part 01
"""

import os
import re
import collections
import argparse
import pprint


def part1(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    joined = ''.join([i.strip() for i in inpt.strip().split('\n')])
    scan = True
    while scan:
        scan = False
        for i in range(len(joined)):
            try:
                j = joined[i+1]
            except IndexError:
                break
            if (ord(joined[i]) - ord(joined[i+1])) in [32, -32]:
                # pop them and keep going
                scan = True
                joined = joined[:i] + joined[i+2:]
    return len(joined)


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    joined = ''.join([i.strip() for i in inpt.strip().split('\n')])
    a_to_z = [re.sub('[%s]' % i, '', joined, flags=re.IGNORECASE) for i in [chr(97 + j) for j in range(26)]]
    minlen = len(max(a_to_z))
    for shorter in a_to_z:
        scan = True
        while scan:
            scan = False
            for i in range(len(shorter)):
                try:
                    j = shorter[i+1]
                except IndexError:
                    break
                if (ord(shorter[i]) - ord(shorter[i+1])) in [32, -32]:
                    # pop them and keep going
                    scan = True
                    shorter = shorter[:i] + shorter[i+2:]
        minlen = min(minlen, len(shorter))
        print(f"New minlen found: {minlen}")
    return minlen


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
