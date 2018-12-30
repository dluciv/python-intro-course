#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from typing import List, Iterable, Tuple, Any
import pygments.lexers.python as plx
import glob
import json
import os
import itertools
import sys
import chardet
from pygments.token import Token


def read_pythons_from_file(filename: str)-> Iterable[str]:
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

    def read_pythons_from_notebook() -> Iterable[str]:
        '''Too lazy to look for Jupyter API'''
        try:
            with open(filename, 'r', encoding='utf-8') as ipynb:
                nbc = json.load(ipynb)
                cells: Iterable = nbc['cells']
                for c in cells:
                    if c['cell_type'] == 'code':
                        src = '\n'.join(
                            l if not l.startswith('%') else '#<%> ' + l
                            for l in c['source']
                        )
                        yield src
        except Exception as e:
            print("Error reading %s" % (filename), repr(e), file=sys.stderr)

    if filename.endswith('.ipynb'):
        yield from read_pythons_from_notebook()
    else:
        try:
            with open(filename, 'r', encoding='utf-8') as py:
                yield read_nasty_file()
        except Exception as e:
            print("Error reading %s" % (filename), repr(e), file=sys.stderr)


def lex_python_source(source_code: str)-> Iterable[Any]:
    '''Get sequence of keywords from python source'''
    lx = plx.Python3Lexer()
    tokens: Iterable[Tuple[Any, Any]] = lx.get_tokens(source_code)
    for ttype, tvalue in tokens:
        if ttype == Token.Text:
            yield '&""'
        elif ttype == Token.Name:
            yield '&name'
        elif ttype == Token.Comment.Single:
            yield '&#'
        else:
            yield str(tvalue)


def globs()-> List[str]:
    filenames = []
    filenames.extend(glob.glob(os.path.join('**', '*.py'), recursive=True))
    filenames.extend(glob.glob(os.path.join('**', '*.ipynb'), recursive=True))
    filenames.sort()
    return filenames


def get_python_sources(filenames: Iterable[str])-> Iterable[Tuple[str, str]]:
    for fn in filenames:
        for pysrc, idx in zip(read_pythons_from_file(fn), itertools.count(0 if fn.endswith('.py') else 1)):
            if len(pysrc.strip()) != 0:
                yield "%s!%02d" % (fn, idx), pysrc


if __name__=='__main__':
    gs = globs()
    print(gs)
    srcs = get_python_sources(gs)
    # print(srcs)
    lexed = [(n, lex_python_source(s)) for n, s in srcs]
    for n, l in lexed:
        try:
            print(n, " ".join(l))
        except Exception as e:
            print(repr(e), file=sys.stderr)
