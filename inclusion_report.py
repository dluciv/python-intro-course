#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import sys
import argparse
from typing import List, Iterable

from sourcedrop import PythonSource


def globs(path: str)-> List[str]:
    filenames = []
    filenames.extend(
        glob.glob(
            os.path.join(
                path,
                '**',
                '*.py'),
            recursive=True))
    filenames.extend(
        glob.glob(
            os.path.join(
                path,
                '**',
                '*.ipynb'),
            recursive=True))
    filenames.sort()
    return filenames


def get_python_sources(
        filenames: Iterable[str], min_lexemes: int)-> Iterable[PythonSource]:
    for fn in filenames:
        for ps in PythonSource.read_pythons_from_file(fn):
            if len(ps.raw_lexemes) >= min_lexemes:
                yield ps


def get_args()-> argparse.Namespace:
    apr = argparse.ArgumentParser()
    apr.add_argument(
        "-g",
        "--good-guys",
        help="Sources of good guys, who code",
        required=True)
    apr.add_argument(
        "-b",
        "--bad-guys",
        help="Sources of presumably bad guys, who can steal",
        required=True)
    apr.add_argument(
        "-t",
        "--borrow-threshold",
        help="Max amount of borrowed code to remain good",
        type=float,
        default=0.2)
    apr.add_argument(
        "-m",
        "--min-length",
        help="Minimal number of tokens in source to teke it in account",
        type=int,
        default=20
    )
    return apr.parse_args()


def workflow():
    args = get_args()

    gs = globs(args.good_guys)  # type: ignore
    bs = globs(args.bad_guys)   # type: ignore
    ts = args.borrow_threshold  # type: ignore
    ml = args.min_length

    good_sources = list(get_python_sources(gs, ml))
    bad_sources = list(get_python_sources(bs, ml))

    total_comparisons = len(good_sources) * len(bad_sources)
    done_comparisons = 0
    for b in bad_sources:
        for g in good_sources:
            borrowed_fraction = b.borrowed_fraction_from(g, False)
            if sys.stdout.isatty():
                print(
                    "%d / %d" %
                    (done_comparisons,
                     total_comparisons),
                    end='\r')
                sys.stdout.flush()
            if borrowed_fraction is not None and borrowed_fraction >= ts:
                print("%02d%% of %s borrowed from %s" % (
                    int(100.0 * borrowed_fraction),
                    b.id_repr,
                    g.id_repr
                ))
            done_comparisons += 1
    # TODO:


if __name__ == '__main__':
    workflow()
