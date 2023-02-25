# -*- coding: utf-8 -*-

import dataclasses
from enum import Enum
import itertools
import json
import sys
import difflib
from io import BytesIO
from typing import Optional, List, Tuple, Iterable
import tokenize
import keyword

import chardet


class LexMode(Enum):
    EXACT_MODE = 'exact'
    TOKENIZE_MODE = 'tokenize'
    IDENTIFIER_STRIP_MODE = 'id-strip'

    def __str__(self):
        return self.value


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
    total_lexemes: int
    fingerprint_lexemes: List[str]

    @property
    def id_repr(self)-> str:
        return\
            "%s[%02d]" % (
                self.file_name,
                self.file_index) if self.file_index is not None else self.file_name

    def borrowed_fraction_from(
            self,
            other: 'PythonSource',
            minimal_match_length: int,
            consider_reordered: bool = True
    )-> Optional[float]:
        """Tells, what fraction of current source was (if it was)
        likely borrowed from another one"""
        
        # Trivial cases
        
        if self is other or self.id_repr == other.id_repr:
            return None
        elif self.fingerprint_lexemes == other.fingerprint_lexemes:
            return 1.0
        
        # Invoke LCS until nothing is borrowed

        # Markers from unicode provate use area,
        # will never occur in source code
        self_marker  = '\uE001'
        other_marker = '\uE002'
        
        self_lexemes = self.fingerprint_lexemes.copy()
        other_lexemes = other.fingerprint_lexemes.copy()
        
        common_size = 0
        
        resultative = True
        while resultative:
            sm = difflib.SequenceMatcher(
                None,
                self_lexemes,
                other_lexemes,
                False
            )  # type: ignore
            
            resultative = False
            for b in sm.get_matching_blocks():
                self_index, other_index, match_size = tuple(b)
                if match_size >= minimal_match_length:

                    # Found something, will try next time
                    # if we consider reordered plagiarism
                    resultative = consider_reordered

                    # Take the match into account
                    common_size += match_size

                    # Make the match different
                    self_lexemes[self_index: self_index + match_size] = [self_marker] * match_size
                    other_lexemes[other_index: other_index + match_size] = [other_marker] * match_size
        
        """
        sm = difflib.SequenceMatcher(
            None,
            self.fingerprint_lexemes,
            other.fingerprint_lexemes,
            False
        )  # type: ignore

        common_size = sum(b.size for b in sm.get_matching_blocks()
                          if b.size >= minimal_match_length)
        """
        
        return float(common_size / len(self.fingerprint_lexemes))

    @staticmethod
    def _lex_python_source(
            source_code: str, lex_mode: LexMode) -> Tuple[List[str], int]:
        """Get sequence of lexemes (depersonated or raw) from python source"""

        fingerprint_lexemes = []

        tokens = list(tokenize.tokenize(
            BytesIO(source_code.encode('utf-8')).readline))

        for ttype, tvalue, tstart, tend, tline in tokens:
            if ttype in (
                    tokenize.INDENT, tokenize.DEDENT, tokenize.NEWLINE,
                    tokenize.NL, tokenize.ENDMARKER, tokenize.ERRORTOKEN
            ):
                continue

            ts = tvalue.strip()

            if lex_mode == LexMode.TOKENIZE_MODE:
                fingerprint_lexemes.append(ts)
            elif lex_mode == LexMode.IDENTIFIER_STRIP_MODE:
                if ttype == tokenize.NAME:
                    if keyword.iskeyword(ts):
                        fingerprint_lexemes.append(ts)
                    else:
                        fingerprint_lexemes.append('&id')
                elif ttype == tokenize.STRING:
                    fingerprint_lexemes.append('&""')
                elif ttype == tokenize.NUMBER:
                    fingerprint_lexemes.append('&num')
                elif ttype == tokenize.COMMENT:
                    fingerprint_lexemes.append('&#')
                else:
                    fingerprint_lexemes.append(ts)
            else:
                raise ValueError(
                    "Lex mode %s not implemented for Python sources" %
                    (lex_mode.value))

        return fingerprint_lexemes, len(tokens)

    @staticmethod
    def read_pythons_from_file(
            filename: str, lex_mode: LexMode)-> Iterable['PythonSource']:
        def read_nasty_file()-> str:
            try:
                with open(filename, 'r', encoding='utf-8') as tf:
                    return tf.read()
            except UnicodeDecodeError as ue:
                print(
                    "Author did not master UTF-8: %s" %
                    (filename), file=sys.stderr)
                with open(filename, 'rb') as bf:
                    bts = bf.read()
                    ec = chardet.detect(bts)
                    print(" - and with confidence of %f used %s" %
                          (ec['confidence'], ec['encoding']), file=sys.stderr)
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
                            fl, tt = PythonSource._lex_python_source(
                                src, lex_mode)
                            yield PythonSource(filename, n, tt, fl)
            except Exception as e:
                print(
                    "Error reading %s" %
                    (filename),
                    repr(e),
                    file=sys.stderr)

        if filename.endswith('.ipynb'):
            yield from read_pythons_from_notebook()

        else:
            try:
                src = read_nasty_file()
                fl, tt = PythonSource._lex_python_source(src, lex_mode)
                yield PythonSource(filename, None, tt, fl)
            except Exception as e:
                print(
                    "Error reading %s" %
                    (filename),
                    repr(e),
                    file=sys.stderr)


if __name__ == '__main__':
    print("This is not a script, just a module", file=sys.stderr)
    exit(-1)
