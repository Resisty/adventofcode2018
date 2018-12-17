#!/usr/bin/env python3
""" Part 01
"""

import os
import re
import collections
import argparse


POINT = collections.namedtuple('Point', 'x y')


def manh(point_a, point_b):
    """ Manhattan distance
    """
    return abs(point_a.x - point_b.x) + abs(point_a.y - point_b.y)


def part1(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    points = [POINT(*[int(i) for i in line.split(', ')]) for line in inpt.strip().split('\n')]
    possible_area_points = set({pnt for pnt in points})
    point_claims = collections.defaultdict(int)
    maxx = max(points, key=lambda x: x.x).x
    maxy = max(points, key=lambda x: x.y).y
    closest_map = collections.defaultdict(list)
    for i in range(maxy + 1):
        for j in range(maxx + 2):
            spot = POINT(j, i)
            mindist = None
            for pnt in points:
                dist = manh(pnt, spot)
                mindist = dist if mindist is None else min(mindist, dist)
            closest_map[spot] = [pnt for pnt in points if manh(pnt, spot) == mindist]
            if len(closest_map[spot]) <= 1:
                point_claims[closest_map[spot][0]] += 1
                # bordering infinite
                if spot.x == 1 or spot.y == 1 or spot.x == maxx + 1 or spot.y == maxy + 1:
                    try:
                        possible_area_points.remove(closest_map[spot][0])
                    except KeyError:
                        pass  # already marked off
    point_claims = {i: j for i, j in point_claims.items() if i in possible_area_points}
    return point_claims[max(point_claims, key=point_claims.get)]


def part2(args):
    """ Solve the puzzle
    """
    inpt = validate_and_open(args.input)
    points = [POINT(*[int(i) for i in line.split(', ')]) for line in inpt.strip().split('\n')]
    possible_area_points = set({pnt for pnt in points})
    point_claims = collections.defaultdict(int)
    maxx = max(points, key=lambda x: x.x).x
    maxy = max(points, key=lambda x: x.y).y
    closest_map = collections.defaultdict(list)
    region_spots = 0
    for i in range(maxy + 1):
        for j in range(maxx + 2):
            if sum([manh(POINT(j, i), pnt) for pnt in points]) < 10000:
                region_spots += 1
    return region_spots


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
