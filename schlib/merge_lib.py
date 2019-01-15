#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
from schlib import *
from pprint import pprint
import argparse, sys
import re
import os

parser = argparse.ArgumentParser(description='Creates library with components from A plus components from B. If component from B already exists in A then it is not added.')
parser.add_argument('lib_a', help='The name of the component to be moved')
parser.add_argument('lib_b', help='The path to the source library')
parser.add_argument('lib_out', help='The path to the destination library')
args = parser.parse_args()

if os.path.isfile(args.lib_out): 
    os.remove(args.lib_out);

# check if the component exists in the source
lib_a = SchLib(args.lib_a)
lib_b = SchLib(args.lib_b)
lib_out = SchLib(args.lib_out, True)

def fix_component(component):
    if component.name in components:
        mpn = filter(lambda x: "fieldname" in x and (x["fieldname"] == "MFN" or x["fieldname"] == "MPN"), component.fields);
        if len(mpn) > 0:
            mpn = mpn[0];
            if mpn["fieldname"] == "MFN":
                #print("Note: Replacing MPN with MFN %s" % mpn["name"]);
                component.fields.append({'fieldname': 'MPN','htext_justify': 'C','name': mpn["name"],'posx': '0','posy': '-300','text_orient': 'H','text_size': '50','visibility': 'I','vtext_justify': 'CNN'})
        else:
            print("Warning: Component %s is missing MPN!" % component.name);

    return component

components = {};

for component in lib_b.components:
    component = fix_component(component);
    components[component.name] = component;    
    #pprint(vars(component))

for component in lib_a.components:
    component = fix_component(component);
    components[component.name] = component;    

l = []
for key in components:
    l.append(components[key]);

l.sort(key=lambda x: x.name);

for component in l:
    print(component.name);
    lib_out.addComponent(component);

lib_out.save();

