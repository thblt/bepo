#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# produit le fichier dead.conf
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#


import sys
import re

import defaults

defaults.xkbFile = sys.argv[1]

import compose
import dead_keys
import xkb
from terminators import terminators, combiningTerminators, spaceTerminators


# find the dead keys used here
dks = set()
for v in xkb.tmplValues.values():
    if v in terminators:
        dks.add(v)

composeDeadKeys = {}
# parse compose to find the chars not supported xkb with the dead keys

fCompose = open(defaults.composeFile)

# Valid compose entry should have at least two <symbols> before colon
validEntryPattern = re.compile(r'<.+>.*<.+>.*:')


for l in fCompose:
    # and "<KP_" not in l and "<underbar>" not in l and "<rightcaret>" not in l and "<leftshoe>" not in l and \
    # "<leftcaret>" not in l and "<rightshoe>" not in l and "<U223C>" not in l:
    if validEntryPattern.match(l) and not l.startswith("XCOMM") and not l.startswith("#") and \
                    "<Multi_key>" not in l and len(l.strip()) != 0:
        seq = re.findall('<([^ ]+)>', l.split(":")[0])
        seq = [compose.upperUnicode(s) for s in seq]
        if compose.areSupportedChars(seq):
            c = l.split(":")[1].split()[1]
            k = tuple(compose.char(n) for n in seq)
            composeDeadKeys[k] = compose.char(c)
# print composeDeadKeys

f = open(sys.argv[2], "w")

for m in sorted([m for m in dead_keys.dmm if len(m) == 1]):
    if m[0] in dks:
        comm = ""
    else:
        comm = "#"
    deadName = "dead_" + m[0].replace("ringabove", "abovering")
    print("# %s" % deadName, file=f)
    print(file=f)
    for k, mods in sorted(dead_keys.dc):
        if mods == m and (k, ()) in dead_keys.dc:
            ck = (m[0], dead_keys.dc[k, ()])
            inCompose = ck in composeDeadKeys
            if inCompose:
                tag = "L!"
                if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
                    print(ck)
            else:
                tag = ""
            print("%s%s%s\t%s\t%s" % (comm, tag, deadName, compose.name(dead_keys.dc[k, ()]),
                                      compose.name(dead_keys.dc[k, mods])), file=f)
        elif m[0] in mods:
            K = (k, tuple(a for a in mods if a != m[0]))
            if K in dead_keys.dc:
                ck = (m[0], dead_keys.dc[K])
                inCompose = ck in composeDeadKeys
                if inCompose:
                    tag = "L!"
                    if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
                        print(ck)
                else:
                    tag = ""
                print("%s%s%s\t%s\t%s" % (comm, tag, deadName, compose.name(dead_keys.dc[K]),
                                          compose.name(dead_keys.dc[k, mods])), file=f)

    # terminators
    if (m[0], m[0]) in composeDeadKeys:
        tag = "L!"
        if composeDeadKeys[(m[0], m[0])] != terminators[m[0]]:
            print(m[0], m[0])
    else:
        tag = ""
    if m[0] in terminators:
        print("%s%s%s\t%s\t%s" % (comm, tag, deadName, deadName, compose.name(terminators[m[0]])), file=f)

    if (m[0], " ") in composeDeadKeys:
        tag = "L!"
        if composeDeadKeys[(m[0], " ")] != terminators[m[0]]:
            print(m[0], "nobreakspace")
    else:
        tag = ""
    if m[0] in terminators:
        print("%s%s%s\t%s\t%s" % (comm, tag, deadName, "nobreakspace", compose.name(combiningTerminators[m[0]])),
              file=f)

    if (m[0], " ") in composeDeadKeys:
        tag = "L!"
        if composeDeadKeys[(m[0], " ")] != spaceTerminators[m[0]]:
            print("Warning:", m[0], "space is different in Compose:", composeDeadKeys[(m[0], " ")],
                  spaceTerminators[m[0]])
    else:
        tag = ""
    if m[0] in terminators:
        print("%s%s%s\t%s\t%s" % (comm, tag, deadName, "space", compose.name(spaceTerminators[m[0]])), file=f)

    print(file=f)

# double dead_keys
for m in sorted([m for m in dead_keys.dmm if len(m) == 2]):
    if m[0] in dks and m[1] in dks:
        comm = ""
    else:
        comm = "#"
    deadNames = tuple("dead_" + m1.replace("ringabove", "abovering") for m1 in m)
    print("# %s" % " & ".join(deadNames), file=f)
    print(file=f)
    for k, mods in sorted(dead_keys.dc):
        if mods == m and (k, ()) in dead_keys.dc:
            # first couple
            ck = (m[0], m[1], dead_keys.dc[k, ()])
            inCompose = ck in composeDeadKeys
            if inCompose:
                tag = "L!"
                if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
                    print(ck)
            else:
                tag = ""
            print("%s%s%s\t%s\t%s\t%s" % (comm, tag, deadNames[0], deadNames[1], compose.name(dead_keys.dc[k, ()]),
                                          compose.name(dead_keys.dc[k, mods])), file=f)

            # second couple
            ck = (m[1], m[0], dead_keys.dc[k, ()])
            inCompose = ck in composeDeadKeys
            if inCompose:
                tag = "L!"
                if composeDeadKeys[ck] != dead_keys.dc[k, mods]:
                    print(ck)
            else:
                tag = ""
            print("%s%s%s\t%s\t%s\t%s" % (comm, tag, deadNames[1], deadNames[0], compose.name(dead_keys.dc[k, ()]),
                                          compose.name(dead_keys.dc[k, mods])), file=f)
    print(file=f)
