#!/usr/bin/env python3
""" Part 01
"""

import os
import re
import collections
import argparse
import pprint
from dateutil import parser


def part1(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    guards = collections.defaultdict(lambda: collections.defaultdict(list))
    guard_sleeps = collections.defaultdict(int)
    max_sleeps = 0
    sleeper = None
    lines = sorted([line for line in inpt.strip().split('\n')])
    for line in lines:
        parsed = re.search(r'\[(.*)\] Guard #(\d+) begins shift', line)
        if parsed:
            # new guard
            groups = parsed.groups()
            gid = groups[1]
            time = parser.parse(groups[0])
            # if not time.hour:
            #     guards[gid][time.minute].append(True)
            continue
        parsed = re.search(r'\[(.*)\] (falls asleep|wakes up)', line)
        if parsed:
            groups = parsed.groups()
            if 'falls' in groups[1]:
                time = parser.parse(groups[0])
                guards[gid][time.minute].append(False)
                guard_sleeps[gid] += 1
            else:
                wakeup = parser.parse(groups[0])
                for minute in range(time.minute + 1, wakeup.minute):
                    guards[gid][minute].append(False)
                    guard_sleeps[gid] += 1
            if guard_sleeps[gid] > max_sleeps:
                max_sleeps = guard_sleeps[gid]
                sleeper = gid
        else:
            print(f'A line didn\'t match anything! "{line}"')
    sleepiest_min = max(guards[sleeper], key=guards[sleeper].get)
    return f'Guard #{sleeper} slept for {max_sleeps}, mostly on {sleepiest_min}. Answer: {int(sleeper) * sleepiest_min}'


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    guards = collections.defaultdict(lambda: collections.defaultdict(list))
    guard_sleeps = collections.defaultdict(int)
    lines = sorted([line for line in inpt.strip().split('\n')])
    for line in lines:
        parsed = re.search(r'\[(.*)\] Guard #(\d+) begins shift', line)
        if parsed:
            # new guard
            groups = parsed.groups()
            gid = groups[1]
            time = parser.parse(groups[0])
            # if not time.hour:
            #     guards[gid][time.minute].append(True)
            continue
        parsed = re.search(r'\[(.*)\] (falls asleep|wakes up)', line)
        if parsed:
            groups = parsed.groups()
            if 'falls' in groups[1]:
                time = parser.parse(groups[0])
                guards[gid][time.minute].append(False)
                guard_sleeps[gid] += 1
            else:
                wakeup = parser.parse(groups[0])
                for minute in range(time.minute + 1, wakeup.minute):
                    guards[gid][minute].append(False)
                    guard_sleeps[gid] += 1
        else:
            print(f'A line didn\'t match anything! "{line}"')
    sleepiest_guard = None
    sleepiest_minute = None
    max_sleeps = 0
    for guard, minute_sleeps in guards.items():
        for minute, sleeps in minute_sleeps.items():
            if len(sleeps) > max_sleeps:
                sleepiest_guard = guard
                sleepiest_minute = minute
                max_sleeps = len(sleeps)
    return f'Guard #{sleepiest_guard} slept on minute {sleepiest_minute}. Answer: {int(sleepiest_guard) * sleepiest_minute}'


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
