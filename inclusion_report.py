#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import glob
import json
import os
import itertools
import sys
import dataclasses
from typing import List, Iterable, Tuple, Any, Optional

import chardet
import pygments.lexers.python as plx
from pygments.token import Token


@dataclasses.dataclass()
class PythonSource:
    """
    To keep a part of Python code

    Attributes:
        file_name Source file name
        file_index Index within filename
        raw_lexemes Lexemes
        fingerprint_lexemes Lexemes with depersonated strings and IDs
    """
    file_name: str
    file_index: Optional[int]
    raw_lexemes: List[str]
    fingerprint_lexemes: List[str]

    @staticmethod
    def _lex_python_source(source_code: str) -> Tuple[List, List]:
        """Get sequence of lexemes (depersonated and raw) from python source"""
        lx = plx.Python3Lexer()
        tokens: Iterable[Tuple[Any, Any]] = lx.get_tokens(source_code)
        raw_lexemes = []
        fingerprint_lexemes = []

        for ttype, tvalue in tokens:
            raw_lexemes.append(tvalue.strip())
            if ttype == Token.Text:
                fingerprint_lexemes.append('&""')
            elif ttype == Token.Name:
                fingerprint_lexemes.append('&name')
            elif ttype == Token.Comment.Single:
                fingerprint_lexemes.append('&#')
            else:
                fingerprint_lexemes.append(str(tvalue))

        return raw_lexemes, fingerprint_lexemes


    @staticmethod
    def read_pythons_from_file(filename: str)-> Iterable['PythonSource']:
        def read_nasty_file()-> str:
            try:
                with open(filename, 'r', encoding='utf-8') as tf:
                    return tf.read()
            except UnicodeDecodeError as ue:
                print("Не осилил(а) UTF-8: %s" % (filename), file=sys.stderr)
                with open(filename, 'rb') as bf:
                    bts = bf.read()
                    ec = chardet.detect(bts)
                    print(" - и на %f использовал(а) %s" % (ec['confidence'], ec['encoding']), file=sys.stderr)
                    return bts.decode(ec['encoding'])

        def read_pythons_from_notebook() -> Iterable['PythonSource']:
            """Too lazy to look for Jupyter API"""
            try:
                with open(filename, 'r', encoding='utf-8') as ipynb:
                    nbc = json.load(ipynb)
                    cells: Iterable = nbc['cells']
                    for c, n in zip(cells, itertools.count()):
                        if c['cell_type'] == 'code':
                            src = '\n'.join(
                                l if not l.startswith('%') else '#<%> ' + l
                                for l in c['source']
                            )
                            rl, fl = PythonSource._lex_python_source(src)
                            yield PythonSource(filename, n, rl, fl)
            except Exception as e:
                print("Error reading %s" % (filename), repr(e), file=sys.stderr)

        if filename.endswith('.ipynb'):
            yield from read_pythons_from_notebook()

        else:
            try:
                src = read_nasty_file()
                rl, fl = PythonSource._lex_python_source(src)
                yield PythonSource(filename, None, rl, fl)
            except Exception as e:
                print("Error reading %s" % (filename), repr(e), file=sys.stderr)


def globs()-> List[str]:
    filenames = []
    filenames.extend(glob.glob(os.path.join('**', '*.py'), recursive=True))
    filenames.extend(glob.glob(os.path.join('**', '*.ipynb'), recursive=True))
    filenames.sort()
    return filenames


def get_python_sources(filenames: Iterable[str])-> Iterable[PythonSource]:
    for fn in filenames:
        yield from PythonSource.read_pythons_from_file(fn)


if __name__ == '__main__':
    gs = globs()
    print(gs)
    srcs = get_python_sources(gs)
    for ps in srcs:
        try:
            print(
                "%s#%02d" % (ps.file_name, ps.file_index) if ps.file_index is not None else ps.file_name,
                " ".join(ps.fingerprint_lexemes)
            )
        except Exception as e:
            print(repr(e), file=sys.stderr)
