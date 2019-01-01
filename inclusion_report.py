#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import os
import sys
import argparse
import multiprocessing
import multiprocessing.dummy
import time
from typing import List, Iterable, Tuple, Optional

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
        "-gg",
        "--good-guys",
        help="Sources of good guys, who code",
        required=True)
    apr.add_argument(
        "-bg",
        "--bad-guys",
        help="Sources of presumably bad guys, who can steal",
        required=True)
    apr.add_argument(
        "-bt",
        "--borrow-threshold",
        help="Max amount of borrowed code to remain good",
        type=float,
        default=0.5)
    apr.add_argument(
        "-ml",
        "--min-length",
        help="Minimal number of tokens in source to teke it in account",
        type=int,
        default=20
    )
    apr.add_argument(
        "-nm",
        "--no-multiprocessing",
        help="No multiprocessing to debug it easily",
        action='store_true',
        required=False
    )
    return apr.parse_args()


def _is_same_guy(bad_filename: str, good_filename: str,
                 bad_root: str, good_root: str)-> bool:
    """If files belong to the same guy to skip the check"""

    bad_root = os.path.normpath(bad_root).\
        lstrip(os.path.sep).rstrip(os.path.sep)
    good_root = os.path.normpath(good_root).\
        lstrip(os.path.sep).rstrip(os.path.sep)

    bad_filename = os.path.normpath(bad_filename).\
        lstrip(os.path.sep).rstrip(os.path.sep)
    good_filename = os.path.normpath(good_filename).\
        lstrip(os.path.sep).rstrip(os.path.sep)

    bad_filename = bad_filename.replace(bad_root + os.path.sep, '')
    good_filename = good_filename.replace(good_root + os.path.sep, '')

    return bad_filename.split(os.path.sep)[0] == \
           good_filename.split(os.path.sep)[0]


_borrow_threshold: float


def compare_srcs(bad_good: Tuple[PythonSource,
                                 PythonSource])-> Tuple[str, str, Optional[float]]:
    global _borrow_threshold
    bad, good = bad_good
    borrowed_fraction = bad.borrowed_fraction_from(good, True)
    return bad.id_repr, good.id_repr, borrowed_fraction


def workflow():
    global _borrow_threshold
    args = get_args()

    gs = globs(args.good_guys)  # type: ignore
    bs = globs(args.bad_guys)   # type: ignore
    _borrow_threshold = args.borrow_threshold  # type: ignore
    ml = args.min_length

    print("Looking for them...")
    good_sources = list(get_python_sources(gs, ml))
    bad_sources = list(get_python_sources(bs, ml))

    tasks: List[Tuple[PythonSource, PythonSource]] = []

    total_comparisons: int = 0
    done_comparisons: int = 0

    print("Capturing them...")
    for b in bad_sources:
        for g in good_sources:
            if not _is_same_guy(b.file_name, g.file_name,
                                args.bad_guys, args.good_guys):
                tasks.append((b, g))
                total_comparisons += 1

    print("Inquiring them...")

    if args.no_multiprocessing:  # type: ignore
        pool = multiprocessing.dummy.Pool(1)
    else:
        pool = multiprocessing.Pool()

    results = pool.imap_unordered(compare_srcs, tasks)

    start_time = time.time()
    for bfn, gfn, bo in results:
        done_comparisons += 1
        if sys.stdout.isatty():
            print(
                "%d / %d, %.2f/sec" %
                (done_comparisons,
                 total_comparisons,
                 done_comparisons / (time.time() - start_time)
                 ),
                end='\r')
            sys.stdout.flush()
        if bo is not None and bo >= _borrow_threshold:
            print("%02d%% of %s borrowed from %s" % (
                int(100.0 * bo),
                bfn,
                gfn
            ))


if __name__ == '__main__':
    workflow()
