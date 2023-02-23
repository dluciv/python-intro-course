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
    
    def lcs(self, str1: str, str2: str):
        max_mapping = 0
        if len(str1) < 3 or len(str2) < 3:
            return 0
        min_length = min(len(str1), len(str2))  # min length or str
        if min_length < 3:
            return 0
        for i in range(3, min_length + 1):
            for k in range(0, len(str1) - i + 1):
                for j in range(0, len(str2) - i + 1):
                    if str1[k:k + i] == str2[j:j + i]:
                        max_mapping = i
        return max_mapping

    def lst_lcs(self, str_list1: list, str_list2: list) -> dict:
        mp = {}
        for row1 in range(0, len(str_list1)):
            for row2 in range(0, len(str_list2)):
                map_len = self.lcs(str_list1[row1], str_list2[row2])
                k = [row1, row2]
                k1 = [row2, row1]
                if mp.has_key(k):
                    if map_len > mp[k]:
                        mp[k] = map_len
                else:
                    mp[k] = map_len
        return mp
    
    def borrowed_fraction_from(
            self, other: 'PythonSource', minimal_match_length: int
    )-> Optional[float]:
        """Tells, what fraction of current source was (if it was)
        likely borrowed from another one"""
        if self is other or self.id_repr == other.id_repr:
            return None
        elif self.fingerprint_lexemes == other.fingerprint_lexemes:
            return 1.0
        
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
        
        mp = self.lst_lcs(self.fingerprint_lexemes, other)
        common_size = sum(v for k, v in mp.items())
       
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
