#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sch import *
import argparse
import csv, sys
from itertools import groupby

parser = argparse.ArgumentParser()
parser.add_argument('sch_file', nargs='+')
parser.add_argument('--out-csv', help='Output csv file', action='store')
args = parser.parse_args()

for f in args.sch_file:
    sch = Schematic(f)

    sch.labels.sort(key=lambda x: x["name"]);
    print("Name,Count");
    for k, g in groupby(sch.labels, lambda x: x["name"]):
        print("%s,%s" % (k, len(list(g))));


