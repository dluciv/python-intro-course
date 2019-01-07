#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import datetime
import glob
import locale
import os
import sys
import argparse
import multiprocessing
import multiprocessing.dummy
import subprocess
from typing import List, Iterable, Tuple, Optional

import tzlocal
import tqdm

from sourcedrop import PythonSource
import report_export


def get_file_mdate(file_name: str)-> datetime.datetime:
    try:
        abs_file_name = os.path.abspath(file_name)
        output: subprocess.Popen = subprocess.Popen(
            ['git', 'log', '--date=iso', '--format="%ad"', '--', abs_file_name],
            stdout=subprocess.PIPE,
            cwd=os.path.split(abs_file_name)[0]
        )
        output.wait(5.0)

        if output.returncode != 0:
            raise UserWarning("Git return code was %d" % (output.returncode))

        bstdout: bytes = output.communicate()[0]
        stdout: Iterable[str] = bstdout.decode(
            locale.getpreferredencoding(False)).split('\n')
        stdout = [l.replace('"', '').replace("'", '').strip() for l in stdout]
        stdout = [l for l in stdout if len(l)]

        last_date: str = stdout[0]
        if last_date.endswith('00'):
            last_date = last_date[:-2] + ':00'

        return datetime.datetime.fromisoformat(last_date)
    except Exception as e:
        print("Error <<%s>> when getting git times for %s" %
              (str(e), file_name), file=sys.stderr)
        return datetime.datetime.utcfromtimestamp(os.path.getmtime(file_name))


def globs(path: str, min_date: Optional[datetime.datetime])-> List[str]:
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

    if min_date:
        filenames = [fn for fn in filenames if get_file_mdate(fn) >= min_date]

    return filenames


def get_python_sources(
        filenames: Iterable[str], min_lexemes: int)-> Iterable[PythonSource]:
    for fn in filenames:
        for ps in PythonSource.read_pythons_from_file(fn):
            if len(ps.raw_lexemes) >= min_lexemes:
                yield ps


def get_args()-> argparse.Namespace:

    # Thanks to https://gist.github.com/monkut/e60eea811ef085a6540f
    def valid_date_type(arg_date_str):
        """custom argparse *date* type for user dates values given from the command line"""
        try:
            given_time = datetime.datetime.strptime(arg_date_str, "%Y-%m-%d")
            tz_time = tzlocal.get_localzone().localize(given_time)
            return tz_time
        except ValueError:
            msg = "Given Date ({0}) not valid! Expected format, YYYY-MM-DD!".format(arg_date_str)
            raise argparse.ArgumentTypeError(msg)

    apr = argparse.ArgumentParser()
    apr.add_argument(
        "-gg",
        "--good-guys",
        help="Sources of good guys, who code",
        required=True
    )
    apr.add_argument(
        "-bg",
        "--bad-guys",
        help="Sources of presumably bad guys, who can steal",
        required=True
    )
    apr.add_argument(
        "-bt",
        "--borrow-threshold",
        help="Max amount of borrowed code to remain good",
        type=float,
        default=0.25
    )
    apr.add_argument(
        "-cm",
        "--check-method",
        help="Check all lexemes or only structure (keywords, etc.) ones",
        choices=['all', 'structure'],
        default='all'
    )
    apr.add_argument(
        "-ml",
        "--min-length",
        help="Minimal number of tokens in source to take it in account",
        type=int,
        default=20
    )
    apr.add_argument(
        "-mml",
        "--min-match-length",
        help="Minimal length of text fragment to take in account",
        type=int,
        default=5
    )
    apr.add_argument(
        "-mbfd",
        "--min-bad-file-date",
        help="Oldest source file of bad guys to consider, older ones will be ignored; format: YYYY-MM-DD",
        type=valid_date_type
    )
    apr.add_argument(
        "-rf",
        "--report-file",
        help="OpenDocument spreadsheet to save the report",
        type=str,
        required=False
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


_minimal_match_length: int = 0
_depersonate_check: bool = False


def compare_srcs(
        settings_bad_good: Tuple[PythonSource, PythonSource]
)-> Tuple[str, str, Optional[float]]:
    global _minimal_match_length, _depersonate_check
    bad, good = settings_bad_good
    borrowed_fraction = bad.borrowed_fraction_from(
        good, _depersonate_check, _minimal_match_length)
    return bad.id_repr, good.id_repr, borrowed_fraction


def compare_srcs_initializer(
        minimal_match_length: int, depersonate_check: bool):
    global _borrow_threshold, _minimal_match_length, _depersonate_check
    _minimal_match_length = minimal_match_length
    _depersonate_check = depersonate_check


def workflow():
    args = get_args()

    borrow_threshold: float = args.borrow_threshold  # type: ignore
    depersonate_check: bool = args.check_method != 'all'  # type: ignore
    minimal_match_length: int = args.min_match_length  # type: ignore

    gs = globs(args.good_guys, None)  # type: ignore
    bs = globs(args.bad_guys, args.min_bad_file_date)   # type: ignore
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
        pool = multiprocessing.dummy.Pool(
            1,
            initializer=compare_srcs_initializer,
            initargs=(minimal_match_length, depersonate_check)
        )
    else:
        pool = multiprocessing.Pool(
            initializer=compare_srcs_initializer,
            initargs=(minimal_match_length, depersonate_check)
        )

    results = pool.imap_unordered(compare_srcs, tasks)

    borrowing_facts: List[Tuple[str, str, float]] = []

    tty = sys.stdout.isatty()
    if tty:
        results = tqdm.tqdm(results, total=total_comparisons)

    for bfn, gfn, bo in results:
        done_comparisons += 1
        if bo is not None and bo >= borrow_threshold:
            borrowing_facts.append((bfn, gfn, bo))
            (results.write if tty else print)(
                "%02d%% of %s borrowed from %s" % (
                    int(100.0 * bo),
                    bfn,
                    gfn
                )
            )
    if args.report_file:
        report_export.export_odf_report(args.report_file, borrowing_facts)


if __name__ == '__main__':
    workflow()
