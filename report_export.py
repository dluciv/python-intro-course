#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import itertools
import math
import sys
import csv
from typing import Iterable, Tuple

from odf.opendocument import OpenDocumentSpreadsheet
from odf.style import Style, TextProperties, ParagraphProperties, TableCellProperties
from odf.style import TableColumnProperties
from odf.text import P, Number
from odf.table import Table, TableColumn, TableRow, TableCell


def export_odf_report(filename: str, borrowing_facts: Iterable[Tuple[str, str, float]]):
    # Thanks to https://joinup.ec.europa.eu/svn/odfpy/tags/release-0.9/api-for-odfpy.odt
    # for example of this API

    doc = OpenDocumentSpreadsheet()

    # -------- add styles -----------
    vertcell = Style(name="vcell", family="table-cell")
    vertcell.addElement(TableCellProperties(rotationangle=90))

    # -------- create table ----------

    # Start the table, and describe the columns
    table = Table(name="Borrowing")

    # ------ process some data ---------

    scols = set(gfn for bfn, gfn, bo in borrowing_facts)
    cols = sorted(scols)
    rows = sorted(set(bfn for bfn, gfn, bo in borrowing_facts))

    rc = {}
    for c, i in zip(cols, itertools.count()):
        rc[c] = i
    rr = {}
    for r, i in zip(rows, itertools.count()):
        rr[r] = i

    data = [[0.0] * len(cols) for r in rows]  # to make different list

    for bfn, gfn, bo in borrowing_facts:
        r = rr[bfn]
        c = rc[gfn]
        data[r][c] = bo

    # --------- go! ----------

    tr = TableRow()

    tc = TableCell()
    tc.addElement(P(text="Borrower \ Source"))
    tr.addElement(tc)

    for c in cols:
        tc = TableCell(stylename=vertcell)
        tc.addElement(P(text=c))
        tr.addElement(tc)

    table.addElement(tr)

    for r, rd in zip(rows, data):
        tr = TableRow()

        tc = TableCell()
        tc.addElement(P(text=r))
        tr.addElement(tc)

        for cd in rd:
            if cd > 0:
                tc = TableCell(valuetype='percentage', value=cd)
            else:
                tc = TableCell()
            tr.addElement(tc)

        table.addElement(tr)

    doc.spreadsheet.addElement(table)
    doc.save(filename, False)


def _export_csv_report(filename: str, borrowing_facts: Iterable[Tuple[str, str, float]]):
    scols = set(gfn for bfn, gfn, bo in borrowing_facts)
    cols = sorted(scols)
    rows = sorted(set(bfn for bfn, gfn, bo in borrowing_facts))

    rc = {}
    for c, i in zip(cols, itertools.count()):
        rc[c] = i
    rr = {}
    for r, i in zip(rows, itertools.count()):
        rr[r] = i

    data = [[0.0] * len(cols) for r in rows]  # to make different list

    for bfn, gfn, bo in borrowing_facts:
        r = rr[bfn]
        c = rc[gfn]
        data[r][c] = bo

    with open(filename, 'w+', encoding='utf-8', newline='') as csvf:
        cw = csv.writer(csvf, dialect='unix', delimiter='\t')
        cw.writerow(["Borrower \ Source"] + cols)

        for r, rd in zip(rows, data):
            cw.writerow([r] + rd)


if __name__ == '__main__':
    print("This is not a script, just a module", file=sys.stderr)
    exit(-1)
