#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Parser pour Compose
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#


import unicodedata, re, sys, defaults

def ishex(s):
    for c in s:
        if c not in "0123456789abcdefABCDEF":
            return False
    return True
    
fKeysymdef = open(defaults.keysymdefFile)

regexp = re.compile(r'#define XK_([^ ]+).*U\+([0-9A-Fa-f]+)')

composeNames = {}

for l in fKeysymdef:
    res = regexp.match(l)
    if res:
        name = res.group(1)
        c = res.group(2)
        try:
            C = chr( int(c, 16) )
            composeNames[name] = C
        except:
            print(l)
            pass
            
# some missing chars
composeNames["combining_acute"] = "́"
composeNames["combining_belowdot"] = "̣"
composeNames["combining_grave"] = "̀"
composeNames["combining_tilde"] = "̃"
composeNames["NoSymbol"] = ""
composeNames["VoidSymbol"] = ""
# dead keys
composeNames["dead_abovedot"] = "abovedot"
composeNames["dead_abovering"] = "ringabove"
composeNames["dead_acute"] = "acute"
composeNames["dead_belowdot"] = "belowdot"
composeNames["dead_breve"] = "breve"
composeNames["dead_caron"] = "caron"
composeNames["dead_cedilla"] = "cedilla"
composeNames["dead_circumflex"] = "circumflex"
composeNames["dead_dasia"] = "dasia"
composeNames["dead_diaeresis"] = "diaeresis"
composeNames["dead_doubleacute"] = "doubleacute"
composeNames["dead_grave"] = "grave"
composeNames["dead_horn"] = "horn"
composeNames["dead_macron"] = "macron"
composeNames["dead_ogonek"] = "ogonek"
composeNames["dead_psili"] = "psili"
composeNames["dead_tilde"] = "tilde"
composeNames["dead_stroke"] = "stroke"
composeNames["dead_currency"] = "currency"
composeNames["Multi_key"] = "Multi_key"
composeNames["dead_greek"] = "greek"
composeNames["dead_belowcomma"] = "commabelow"
composeNames["dead_hook"] = "hook"
composeNames["dead_horn"] = "horn"
composeNames["dead_belowdot"] = "belowdot"

composeChars = {}
for name, C in composeNames.items():
    composeChars[C] = name
# force oslash name
composeChars["ø"] = "oslash"

from terminators import terminators


def char(k):
    if k == '' or k == '#':
        return ''
    if k not in composeNames and k[0] == 'U' and len(k) >= 4 and ishex(k[1:]):
        C = chr(int(k[1:], 16))
        k = k.upper()
        if C in composeChars:
            return C
        composeNames[k] = C
        composeChars[C] = k
    return composeNames[k]

def name(c):
    if c in composeChars:
        return composeChars[c]
    k = "U"+repr(c)[4:-1].rjust(4, '0').upper()
    composeNames[k] = c
    composeChars[c] = k
    return k

def isSupportedChar(k):
    if k[0] == 'U' and len(k) == 5 and ishex(k[1:]):
        return True
    return k in composeNames
    
def areSupportedChars(ks):
    for k in ks:
        if not isSupportedChar(k):
            return False
    return True

def upperUnicode(k):
    if k[0] == 'U' and 5 <= len(k) <= 6 and ishex(k[1:]):
        return k.upper()
    return k
    
fCompose = open(defaults.composeFile)

states = set()
outputs = {}

for l in fCompose:
    if l.startswith("<Multi_key>") and "<KP_" not in l and "<underbar>" not in l and "<rightcaret>" not in l and "<leftshoe>" not in l and "<leftcaret>" not in l and "<rightshoe>" not in l and "<U223C>" not in l:
        seq = re.findall('<([^ ]+)>', l.split(":")[0])
        seq = [upperUnicode(s) for s in seq]
        if areSupportedChars(seq):
            for i in range(1, len(seq)):
                s = tuple(seq[:i])
                states.add(s)
            c = l.split(":")[1].split()[1]
            outputs[tuple(seq)] = char(c)
        
#    for k in seq:
#      if k[0] == 'U' and len(k) == 5 and ishex(k[1:]):
#        k = unichr(int(k[1:], 16))
#      keys.add(k)

statesByAction = {}
for S in states:
    a = S[-1]
    s = S[:-1]
    sset = statesByAction.get(a, set())
    sset.add(s)
    statesByAction[a] = sset


outputsByAction = {}
for S in list(outputs.keys()):
    a = S[-1]
    s = S[:-1]
    sset = outputsByAction.get(a, set())
    sset.add((s, outputs[S]))
    outputsByAction[a] = sset

charActions = {}
for a in set(list(statesByAction.keys()) + list(outputsByAction.keys())):
    # Check there are no items have different name but same unicode point
    # For instance, we once had both includedin and U2282 in the Compose file
    if char(a) in charActions :
        print((a, char(a), charActions[char(a)]))
    charActions[char(a)] = a
# print charActions[u'(']
# sys.exit()

if __name__ == "__main__":
    for a in sorted(set(list(statesByAction.keys()) + list(outputsByAction.keys())) ):
        C = char(a)
        if C:
            print('    <action id="%s">' % C)
            if a in statesByAction:
                for s in sorted(statesByAction[a]):
                    print('      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,))))
            if a in outputsByAction:
                for s, c in sorted(outputsByAction[a]):
                    print('      <when state="%s" output="%s"/>' % ('_'.join(s), c))
            print('    </action>')

            
    print('''
        <action id="Multikey">
            <when state="none" next="Multikey"/>
        </action>
    ''')

    print("  <terminators>")
    for ss in sorted(states):
        C = ''.join([terminators.get(char(s), char(s)) for s in ss])
        s = '_'.join(list(ss))
        print('    <when state="%s" output="%s"/>' % (s, C))
    print("  </terminators>")
    
    
