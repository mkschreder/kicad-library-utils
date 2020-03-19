#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from sch import *
import argparse
import csv, sys

parser = argparse.ArgumentParser()
parser.add_argument('sch_file', nargs='+')
parser.add_argument('--out-csv', help='Output csv file', action='store')
args = parser.parse_args()

for f in args.sch_file:
    sch = Schematic(f)

    comps = [];
    for component in sch.components:
        # check if is power related component
        if '#PWR' in component.fields[0]['ref'] or\
           'PWR_FLAG' in component.fields[1]['ref']:
            continue
        comps.append(component); 

    comps.sort(key=lambda x: x.fields[0]['ref']);
    print("Ref,Name,MPN,Footprint,Datasheet");
    for c in comps:
        print("%s,%s,%s,%s,%s" % (c.fields[0]['ref'], c.fields[1]['ref'], (c.field("MPN") or {"ref": "N/A"})["ref"], c.fields[2]['ref'], c.fields[3]['ref']));
