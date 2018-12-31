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


def get_python_sources(filenames: Iterable[str])-> Iterable[PythonSource]:
    for fn in filenames:
        yield from PythonSource.read_pythons_from_file(fn)


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
    return apr.parse_args()


def workflow():
    args = get_args()

    gs = globs(args.good_guys)  # type: ignore
    bs = globs(args.bad_guys)   # type: ignore
    ts = args.borrow_threshold  # type: ignore

    print(gs)
    srcs = get_python_sources(gs + bs)
    for ps in srcs:
        try:
            print(
                "%s#%02d" % (
                    ps.file_name,
                    ps.file_index) if ps.file_index is not None else ps.file_name,
                " ".join(ps.fingerprint_lexemes)
            )
        except Exception as e:
            print(repr(e), file=sys.stderr)


if __name__ == '__main__':
    workflow()
