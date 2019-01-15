#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from schlib import *
from pprint import pprint
import argparse, sys
import re
import os
import csv 

parser = argparse.ArgumentParser(description='Exports custom fields from all components in a library into a csv file')
parser.add_argument('library', help='The name of the library')
parser.add_argument('csv', help='The name of the csv file')
args = parser.parse_args()

if os.path.isfile(args.csv): 
    os.remove(args.csv);

# check if the component exists in the source
lib = SchLib(args.library)

fieldnames = {"NAME": "", "FOOTPRINT": ""};
records = {};

for component in lib.components:
    fields = {};
    fields["FOOTPRINT"] = component.fields[2]["name"];

    for field in component.fields:
        if "fieldname" in field and len(field["fieldname"]):
            fieldnames[field["fieldname"]] = "";
            fields[field["fieldname"]] = field["name"];

    rec = {"NAME": component.name};
    rec.update(fields);

    records[component.name] = rec;

with open(args.csv, 'wb') as f:
    writer = csv.writer(f);

    lines = []
    for key in records:
        rec = records[key];
        line = [];
        for key in fieldnames:
            if key in rec:
                line.append(rec[key]);
            else:
                line.append("");
        lines.append(line);
    writer.writerow(fieldnames.keys());
    writer.writerows(lines);

