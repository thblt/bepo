#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Génération de touches mortes pour mac os
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#


import re
import unicodedata
from io import StringIO

import compose
import xkb

# the reg exp used to parse the unicode name
chrRegExp = re.compile(r'LATIN (CAPITAL|SMALL) LETTER (.+)')

finalModNamesExceptions = {
    'DOT ABOVE': 'abovedot',
    'DOT BELOW': 'belowdot',
}


def finalModName(n):
    return finalModNamesExceptions.get(n, n).replace(" ", "").replace("-", "").lower()


currency = {
    'LATIN CAPITAL LETTER A WITH CURRENCY': '₳',
    'LATIN SMALL LETTER A WITH CURRENCY': '؋',
    'LATIN CAPITAL LETTER B WITH CURRENCY': '₱',
    'LATIN SMALL LETTER B WITH CURRENCY': '฿',
    'LATIN CAPITAL LETTER C WITH CURRENCY': '₡',
    'LATIN SMALL LETTER C WITH CURRENCY': '¢',
    'LATIN CAPITAL LETTER C WITH CURRENCY AND CEDILLA': '₵',
    'LATIN SMALL LETTER C WITH CURRENCY AND CEDILLA': '₵',
    'LATIN CAPITAL LETTER D WITH CURRENCY': '₯',
    'LATIN SMALL LETTER D WITH CURRENCY': '₫',
    'LATIN CAPITAL LETTER E WITH CURRENCY': '₠',
    'LATIN SMALL LETTER E WITH CURRENCY': '€',
    'LATIN CAPITAL LETTER F WITH CURRENCY': '₣',
    'LATIN SMALL LETTER F WITH CURRENCY': 'ƒ',
    'LATIN CAPITAL LETTER G WITH CURRENCY': '₲',
    'LATIN SMALL LETTER G WITH CURRENCY': '₲',
    'LATIN CAPITAL LETTER H WITH CURRENCY': '₴',
    'LATIN SMALL LETTER H WITH CURRENCY': '₴',
    'LATIN CAPITAL LETTER I WITH CURRENCY': '៛',
    'LATIN SMALL LETTER I WITH CURRENCY': '﷼',
    'LATIN CAPITAL LETTER K WITH CURRENCY': '₭',
    'LATIN SMALL LETTER K WITH CURRENCY': '₭',
    'LATIN CAPITAL LETTER L WITH CURRENCY': '₤',
    'LATIN SMALL LETTER L WITH CURRENCY': '£',
    'LATIN CAPITAL LETTER M WITH CURRENCY': 'ℳ',
    'LATIN SMALL LETTER M WITH CURRENCY': '₥',
    'LATIN CAPITAL LETTER N WITH CURRENCY': '₦',
    'LATIN SMALL LETTER N WITH CURRENCY': '₦',
    'LATIN CAPITAL LETTER O WITH CURRENCY': '૱',
    'LATIN SMALL LETTER O WITH CURRENCY': '௹',
    'LATIN CAPITAL LETTER P WITH CURRENCY': '₧',
    'LATIN SMALL LETTER P WITH CURRENCY': '₰',
    'LATIN CAPITAL LETTER R WITH CURRENCY': '₨',
    'LATIN SMALL LETTER R WITH CURRENCY': '₢',
    'LATIN CAPITAL LETTER S WITH CURRENCY': '$',
    'LATIN SMALL LETTER S WITH CURRENCY': '₪',
    'LATIN CAPITAL LETTER T WITH CURRENCY': '₮',
    'LATIN SMALL LETTER T WITH CURRENCY': '৳',
    'LATIN CAPITAL LETTER THORN WITH CURRENCY': '৲',
    'LATIN SMALL LETTER THORN WITH CURRENCY': '৲',
    'LATIN CAPITAL LETTER U WITH CURRENCY': '圓',
    'LATIN SMALL LETTER U WITH CURRENCY': '元',
    'LATIN CAPITAL LETTER W WITH CURRENCY': '₩',
    'LATIN SMALL LETTER W WITH CURRENCY': '₩',
    'LATIN CAPITAL LETTER Y WITH CURRENCY': '円',
    'LATIN SMALL LETTER Y WITH CURRENCY': '¥',
}

circumflex = {
    'LATIN CAPITAL LETTER 0': '0',
    'LATIN CAPITAL LETTER 0 WITH CIRCUMFLEX': '⁰',
    'LATIN CAPITAL LETTER 1': '1',
    'LATIN CAPITAL LETTER 1 WITH CIRCUMFLEX': '¹',
    'LATIN CAPITAL LETTER 2': '2',
    'LATIN CAPITAL LETTER 2 WITH CIRCUMFLEX': '²',
    'LATIN CAPITAL LETTER 3': '3',
    'LATIN CAPITAL LETTER 3 WITH CIRCUMFLEX': '³',
    'LATIN CAPITAL LETTER 4': '4',
    'LATIN CAPITAL LETTER 4 WITH CIRCUMFLEX': '⁴',
    'LATIN CAPITAL LETTER 5': '5',
    'LATIN CAPITAL LETTER 5 WITH CIRCUMFLEX': '⁵',
    'LATIN CAPITAL LETTER 6': '6',
    'LATIN CAPITAL LETTER 6 WITH CIRCUMFLEX': '⁶',
    'LATIN CAPITAL LETTER 7': '7',
    'LATIN CAPITAL LETTER 7 WITH CIRCUMFLEX': '⁷',
    'LATIN CAPITAL LETTER 8': '8',
    'LATIN CAPITAL LETTER 8 WITH CIRCUMFLEX': '⁸',
    'LATIN CAPITAL LETTER 9': '9',
    'LATIN CAPITAL LETTER 9 WITH CIRCUMFLEX': '⁹',
    'LATIN CAPITAL LETTER +': '+',
    'LATIN CAPITAL LETTER + WITH CIRCUMFLEX': '⁺',
    'LATIN CAPITAL LETTER (': '(',
    'LATIN CAPITAL LETTER ( WITH CIRCUMFLEX': '⁽',
    'LATIN CAPITAL LETTER )': ')',
    'LATIN CAPITAL LETTER ) WITH CIRCUMFLEX': '⁾',
    'LATIN CAPITAL LETTER =': '=',
    'LATIN CAPITAL LETTER = WITH CIRCUMFLEX': '⁼',
    'LATIN CAPITAL LETTER -': '-',
    'LATIN CAPITAL LETTER - WITH CIRCUMFLEX': '⁻',
}

caron = {
    'LATIN CAPITAL LETTER 0 WITH CARON': '₀',
    'LATIN CAPITAL LETTER 1 WITH CARON': '₁',
    'LATIN CAPITAL LETTER 2 WITH CARON': '₂',
    'LATIN CAPITAL LETTER 3 WITH CARON': '₃',
    'LATIN CAPITAL LETTER 4 WITH CARON': '₄',
    'LATIN CAPITAL LETTER 5 WITH CARON': '₅',
    'LATIN CAPITAL LETTER 6 WITH CARON': '₆',
    'LATIN CAPITAL LETTER 7 WITH CARON': '₇',
    'LATIN CAPITAL LETTER 8 WITH CARON': '₈',
    'LATIN CAPITAL LETTER 9 WITH CARON': '₉',
    'LATIN CAPITAL LETTER + WITH CARON': '₊',
    'LATIN CAPITAL LETTER ( WITH CARON': '₍',
    'LATIN CAPITAL LETTER ) WITH CARON': '₎',
    'LATIN CAPITAL LETTER = WITH CARON': '₌',
    'LATIN CAPITAL LETTER - WITH CARON': '₋',
}

stroke = {
    'LATIN CAPITAL LETTER 2 WITH STROKE': 'ƻ',
    'LATIN CAPITAL LETTER LESS': '<',
    'LATIN CAPITAL LETTER LESS WITH STROKE': '≮',
    'LATIN CAPITAL LETTER GREATER': '>',
    'LATIN CAPITAL LETTER GREATER WITH STROKE': '≯',
    'LATIN CAPITAL LETTER = WITH STROKE': '≠',
    'LATIN CAPITAL LETTER GREATER OR EQUAL': '≥',
    'LATIN CAPITAL LETTER GREATER OR EQUAL WITH STROKE': '≱',
    'LATIN CAPITAL LETTER LESS OR EQUAL': '≤',
    'LATIN CAPITAL LETTER LESS OR EQUAL WITH STROKE': '≰',
    # missing chars in python 2.5 unicode
    'LATIN SMALL LETTER A WITH STROKE': 'ⱥ',
    'LATIN CAPITAL LETTER B WITH STROKE': 'Ƀ',
    'LATIN CAPITAL LETTER E WITH STROKE': 'Ɇ',
    'LATIN SMALL LETTER E WITH STROKE': 'ɇ',
    'LATIN CAPITAL LETTER J WITH STROKE': 'Ɉ',
    'LATIN SMALL LETTER J WITH STROKE': 'ɉ',
    'LATIN CAPITAL LETTER P WITH STROKE': 'Ᵽ',
    'LATIN CAPITAL LETTER R WITH STROKE': 'Ɍ',
    'LATIN SMALL LETTER R WITH STROKE': 'ɍ',
    'LATIN CAPITAL LETTER U WITH STROKE': 'Ʉ',
    'LATIN SMALL LETTER U WITH STROKE': 'ʉ',
    'LATIN CAPITAL LETTER Y WITH STROKE': 'Ɏ',
    'LATIN SMALL LETTER Y WITH STROKE': 'ɏ',
}

greek = {
    'LATIN CAPITAL LETTER A WITH GREEK': 'Α',
    'LATIN SMALL LETTER A WITH GREEK': 'α',
    'LATIN CAPITAL LETTER B WITH GREEK': 'Β',
    'LATIN SMALL LETTER B WITH GREEK': 'β',
    'LATIN CAPITAL LETTER D WITH GREEK': 'Δ',
    'LATIN SMALL LETTER D WITH GREEK': 'δ',
    'LATIN CAPITAL LETTER E WITH GREEK': 'Ε',
    'LATIN SMALL LETTER E WITH GREEK': 'ε',
    'LATIN CAPITAL LETTER F WITH GREEK': 'Φ',
    'LATIN SMALL LETTER F WITH GREEK': 'φ',
    'LATIN CAPITAL LETTER G WITH GREEK': 'Γ',
    'LATIN SMALL LETTER G WITH GREEK': 'γ',
    'LATIN CAPITAL LETTER H WITH GREEK': 'Η',
    'LATIN SMALL LETTER H WITH GREEK': 'η',
    'LATIN CAPITAL LETTER I WITH GREEK': 'Ι',
    'LATIN SMALL LETTER I WITH GREEK': 'ι',
    'LATIN CAPITAL LETTER J WITH GREEK': 'Θ',
    'LATIN SMALL LETTER J WITH GREEK': 'θ',
    'LATIN CAPITAL LETTER K WITH GREEK': 'Κ',
    'LATIN SMALL LETTER K WITH GREEK': 'κ',
    'LATIN CAPITAL LETTER L WITH GREEK': 'Λ',
    'LATIN SMALL LETTER L WITH GREEK': 'λ',
    'LATIN CAPITAL LETTER M WITH GREEK': 'Μ',
    'LATIN SMALL LETTER M WITH GREEK': 'μ',
    'LATIN CAPITAL LETTER N WITH GREEK': 'Ν',
    'LATIN SMALL LETTER N WITH GREEK': 'ν',
    'LATIN CAPITAL LETTER O WITH GREEK': 'Ο',
    'LATIN SMALL LETTER O WITH GREEK': 'ο',
    'LATIN CAPITAL LETTER P WITH GREEK': 'Π',
    'LATIN SMALL LETTER P WITH GREEK': 'π',
    'LATIN CAPITAL LETTER Q WITH GREEK': 'Χ',
    'LATIN SMALL LETTER Q WITH GREEK': 'χ',
    'LATIN CAPITAL LETTER R WITH GREEK': 'Ρ',
    'LATIN SMALL LETTER R WITH GREEK': 'ρ',
    'LATIN CAPITAL LETTER S WITH GREEK': 'Σ',
    'LATIN SMALL LETTER S WITH GREEK': 'σ',
    'LATIN CAPITAL LETTER T WITH GREEK': 'Τ',
    'LATIN SMALL LETTER T WITH GREEK': 'τ',
    'LATIN CAPITAL LETTER U WITH GREEK': 'Υ',
    'LATIN SMALL LETTER U WITH GREEK': 'υ',
    'LATIN CAPITAL LETTER W WITH GREEK': 'Ω',
    'LATIN SMALL LETTER W WITH GREEK': 'ω',
    'LATIN CAPITAL LETTER X WITH GREEK': 'Ξ',
    'LATIN SMALL LETTER X WITH GREEK': 'ξ',
    'LATIN CAPITAL LETTER Y WITH GREEK': 'Ψ',
    'LATIN SMALL LETTER Y WITH GREEK': 'ψ',
    'LATIN CAPITAL LETTER Z WITH GREEK': 'Ζ',
    'LATIN SMALL LETTER Z WITH GREEK': 'ζ',
    # double diacritic
    'LATIN CAPITAL LETTER U WITH GREEK AND HOOK': 'ϒ',
    # 03D3;GREEK UPSILON WITH ACUTE AND HOOK SYMBOL;Lu;0;L;03D2 0301;;;;N;GREEK CAPITAL LETTER UPSILON HOOK TONOS;;;;
    # 03D4;GREEK UPSILON WITH DIAERESIS AND HOOK SYMBOL;Lu;0;L;03D2 0308;;;;N;GREEK CAPITAL LETTER UPSILON HOOK DIAERESIS;;;;
    'LATIN SMALL LETTER R WITH GREEK AND STROKE': 'ϼ',
    'LATIN SMALL LETTER A WITH GREEK AND MACRON': 'ᾱ',
    'LATIN CAPITAL LETTER A WITH GREEK AND MACRON': 'Ᾱ',
    'LATIN SMALL LETTER I WITH GREEK AND MACRON': 'ῑ',
    'LATIN CAPITAL LETTER I WITH GREEK AND MACRON': 'Ῑ',
    'LATIN SMALL LETTER U WITH GREEK AND MACRON': 'ῡ',
    'LATIN CAPITAL LETTER U WITH GREEK AND MACRON': 'Ῡ',
}

tilde = {
    'LATIN CAPITAL LETTER - WITH TILDE': '≃',
    'LATIN CAPITAL LETTER LESS WITH TILDE': '≲',
    'LATIN CAPITAL LETTER GREATER WITH TILDE': '≳',
}

hook = {
    'LATIN CAPITAL LETTER M WITH HOOK': 'Ɱ',
    'LATIN SMALL LETTER W WITH HOOK': 'ⱳ',
    'LATIN CAPITAL LETTER W WITH HOOK': 'Ⱳ',
}

from terminators import terminators, combiningTerminators, spaceTerminators


# 'STRIKETHROUGH',
# 'SMALL LETTER J':,
# 'SMALL LETTER Z',


def case_order(a, b):
    if a[0] != b[0]:
        return cmp(a, b)
    return cmp(b[1], a[1])


def mod_order(a, b):
    if len(a) == len(b):
        return cmp(a, b)
    return cmp(len(a), len(b))


def mod_order2(a, b):
    if a[0] == b[0]:
        return 0
    if a[0] == 'none':
        return -1
    if b[0] == 'none':
        return 1
    return cmp(a, b)


# create the unicode dict, with extended chars for the dead keys
# key: the unicode name (str)
# value: the unicode char (unicode)
unicode_dict = {}
for c in range(0, 0x10000):
    C = chr(c)
    try:
        name = unicodedata.name(C)
    except:
        continue
    if name.startswith('LATIN '):
        unicode_dict[name] = C
# append the currency signs
unicode_dict.update(currency)
unicode_dict.update(circumflex)
unicode_dict.update(caron)
unicode_dict.update(stroke)
unicode_dict.update(greek)
unicode_dict.update(tilde)
unicode_dict.update(hook)


# iterate over all the items to build the set of modifiers for the
# basic latin characters, and the set of modifiers
#
# The result is stored in d
# key: a tuple where the first item is the letter name, and the second
# is "SMALL" or "CAPITAL". Ex: ('W', 'CAPITAL')
# value: a set of tuple of modifiers. Ex: set([('acute',), ('circumflex',),
# ('acute', 'circumflex'), ()]). The modifiers or ordered in the tuple.
#
d = {}

# the dictionnary which associate the char, case, and modifiers to an unicode
# character
# key: ( ( name, case), (mod1, mod2, ...) )
# value: an unicode char
dc = {}

# the set of modifiers used
dm = set()

# the set of sets of modifiers
dmm = set()

for name, C in unicode_dict.items():
    # to register the name in compose
    compose.name(C)
    # split the name and the modifiers
    ns = name.split(' WITH ')
    n = ns[0]
    ms = ' AND '.join(ns[1:])
    modifiers = ms.split(' AND ')
    # some chars have a WITH to describe something which is not a modifier
    for m in ['SMALL LETTER J', 'SMALL LETTER Z', 'STRIKETHROUGH']:
        if m in modifiers:
            n = n + ' WITH ' + m
            modifiers.remove(m)
    # translate the dotless modifier to dot above.
    if 'DOTLESS' in n:
        n = n.replace('DOTLESS ', '')
        modifiers.append('DOT ABOVE')
    # translate the middle dot modifier to dot above
    if 'MIDDLE DOT' in modifiers:
        del modifiers[modifiers.index('MIDDLE DOT')]
        modifiers.append('DOT ABOVE')
    # translate hook above to hook
    if 'HOOK ABOVE' in modifiers:
        del modifiers[modifiers.index('HOOK ABOVE')]
        modifiers.append('HOOK')
    # translate left hook to hook
    if 'LEFT HOOK' in modifiers:
        del modifiers[modifiers.index('LEFT HOOK')]
        modifiers.append('HOOK')
    # remove empty string in the modifier, to generate an empty tuple
    if '' in modifiers:
        modifiers.remove('')
    # translate the modifier names to there final name, sort the modifiers, and
    # and convert the list to a tuple
    modifiers = [finalModName(m) for m in modifiers]
    modifiers = sorted(modifiers)
    modifiers = tuple(modifiers)

    # store the modifiers independently
    for m in modifiers:
        dm.add(m)
    # and store the modifier set
    dmm.add(modifiers)

    m = chrRegExp.match(n)
    if m:
        # print m.group(1), m.group(2), m.group(3)
        case = m.group(1)
        letter = m.group(2)

        key = (letter, case)
        modSet = d.get(key, set([]))
        if modifiers in modSet:
            # print >> sys.stderr, name, "est déjà défini."
            # #, dc[ (key, modifiers) ], C, max( dc[ (key, modifiers) ], C )
            if C in "ỷƴỶƳ":
                dc[(key, modifiers)] = max(dc[(key, modifiers)], C)
            else:
                dc[(key, modifiers)] = min(dc[(key, modifiers)], C)
        else:
            dc[(key, modifiers)] = C
        modSet.add(modifiers)
        d[key] = modSet


# now generate the xml code!
#

def xmlChar(v):
    if v == '"':
        v = "&#x0022;"
    elif v == '<':
        v = "&#x003c;"
    elif v == '&':
        v = '&#x0026;'
    return v


deadXMLBuf = StringIO()

print(file=deadXMLBuf)
print("  <actions>", file=deadXMLBuf)

# store the previous character to print >> deadXMLBuf, a blank line bitween the chars
previous = None

# store the actions already print >> deadXMLBuf,ed. Space and nbsp are aleady there because they are
# special case treated at the end.
actions = set([' ', ' '])

# , case_order):
for c in sorted(list(d.keys())):
    if len(d[c]) != 1 or len(c[0]) == 1:
        if tuple([]) in d[c]:
            if dc[c, tuple([])].lower() != previous:
                print(file=deadXMLBuf)
            print('    <action id="%s">' % xmlChar(dc[c, tuple([])]), file=deadXMLBuf)
            # , mod_order):
            for mod in sorted(d[c]):
                # print >> deadXMLBuf, '    ', '_'.join([finalModNames[m] for m in mod]), dc[ c, mod ]
                if len(mod) == 0:
                    fm = 'none'
                else:
                    fm = '_'.join(mod)
                print('      <when state="%s" output="%s"/>' % (fm, xmlChar(dc[c, mod])), file=deadXMLBuf)

            C = dc[c, tuple([])]
            if C in compose.charActions:
                a = compose.charActions[C]
                if a in compose.statesByAction:
                    for s in sorted(compose.statesByAction[a]):
                        print('      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,))), file=deadXMLBuf)
                if a in compose.outputsByAction:
                    for s, c1 in sorted(compose.outputsByAction[a]):
                        print('      <when state="%s" output="%s"/>' % ('_'.join(s), xmlChar(c1)), file=deadXMLBuf)

            print('    </action>', file=deadXMLBuf)
            actions.add(C)

            # generate the code for 2 modifiers, when a char with on of the 2 diacritic sign
            # is produced
            subd = {}
            for mod in [m for m in d[c] if len(m) == 2]:
                for m1 in mod:
                    if (m1,) in d[c]:
                        for m2 in mod:
                            if m1 != m2:
                                l = subd.get(dc[c, (m1,)], [])
                                l.append((m2, dc[c, mod]))
                                subd[dc[c, (m1,)]] = l
            for c1 in sorted(subd.keys()):
                print('    <action id="%s">' % xmlChar(c1), file=deadXMLBuf)
                print('      <when state="%s" output="%s"/>' % ('none', xmlChar(c1)), file=deadXMLBuf)
                for m, c2 in sorted(subd[c1]):
                    print('      <when state="%s" output="%s"/>' % (m, xmlChar(c2)), file=deadXMLBuf)

                if c1 in compose.charActions:
                    a = compose.charActions[c1]
                    if a in compose.statesByAction:
                        for s in sorted(compose.statesByAction[a]):
                            next_state = '_'.join(s+(a,))
                            print('      <when state="%s" next="%s"/>' % ('_'.join(s), next_state), file=deadXMLBuf)
                    if a in compose.outputsByAction:
                        for s, C in sorted(compose.outputsByAction[a]):
                            print('      <when state="%s" output="%s"/>' % ('_'.join(s), xmlChar(C)), file=deadXMLBuf)

                print('    </action>', file=deadXMLBuf)
                actions.add(c1)
            previous = dc[c, tuple([])].lower()
        else:
            raise ' '.join(c)(d[c])
#  else:
#    print >> deadXMLBuf, '*********************************************', c


# actions with multi keys and without dead keys
for C in sorted(set(list(compose.charActions.keys()) + list(xkb.chars)) - actions - set(["Multi_key"])):
    a = compose.composeChars.get(C, C)
    if C not in terminators:
        print(file=deadXMLBuf)
        print('    <action id="%s">' % xmlChar(C), file=deadXMLBuf)
        print('      <when state="none" output="%s"/>' % xmlChar(C), file=deadXMLBuf)
        if a in compose.statesByAction:
            for s in sorted(compose.statesByAction[a]):
                print('      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,))), file=deadXMLBuf)
        if a in compose.outputsByAction:
            for s, c1 in sorted(compose.outputsByAction[a]):
                print('      <when state="%s" output="%s"/>' % ('_'.join(s), xmlChar(c1)), file=deadXMLBuf)
        print('    </action>', file=deadXMLBuf)


# the space char produces the terminator char when a dead_ states is activated
print(file=deadXMLBuf)
print('    <action id=" ">', file=deadXMLBuf)
print('      <when state="none" output=" "/>', file=deadXMLBuf)
# , mod_order):
for m in sorted(dmm):
    if m != tuple():
        output = ''.join([xmlChar(spaceTerminators.get(n, "?")) for n in m])
        print('      <when state="%s" output="%s"/>' % ('_'.join(m), output), file=deadXMLBuf)
if ' ' in compose.charActions:
    a = compose.charActions[' ']
    if a in compose.statesByAction:
        for s in sorted(compose.statesByAction[a]):
            print('      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,))), file=deadXMLBuf)
    if a in compose.outputsByAction:
        for s, C in sorted(compose.outputsByAction[a]):
            print('      <when state="%s" output="%s"/>' % ('_'.join(s), xmlChar(C)), file=deadXMLBuf)
print('    </action>', file=deadXMLBuf)


# the space char produces the terminator char when a dead_ states is activated
print(file=deadXMLBuf)
print('    <action id=" "> <!-- nbsp -->', file=deadXMLBuf)
print('      <when state="none" output=" "/>', file=deadXMLBuf)
# , mod_order):
for m in sorted(dmm):
    if m != tuple():
        output = ''.join([xmlChar(combiningTerminators.get(n, "?")) for n in m])
        print('      <when state="%s" output="%s"/>' % ('_'.join(m), output), file=deadXMLBuf)
if ' ' in compose.charActions:
    a = compose.charActions[' ']
    if a in compose.statesByAction:
        for s in sorted(compose.statesByAction[a]):
            print('      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,))), file=deadXMLBuf)
    if a in compose.outputsByAction:
        for s, C in sorted(compose.outputsByAction[a]):
            print('      <when state="%s" output="%s"/>' % ('_'.join(s), xmlChar(C)), file=deadXMLBuf)
print('    </action>', file=deadXMLBuf)


modStates = {}
for m in dm:
    modStates[m] = [('none', m)]

# , mod_order):
for m in sorted(dmm):
    if len(m) == 2:
        m1, m2 = m
        modStates[m1].append((m2, '%s_%s' % (m1, m2)))
        modStates[m2].append((m1, '%s_%s' % (m1, m2)))

print(file=deadXMLBuf)
print(file=deadXMLBuf)
for m in sorted(modStates.keys()):
    l = modStates[m]
    print('    <action id="%s">' % m, file=deadXMLBuf)
    print('      <when state="%s" output="%s"/>' % (m, xmlChar(terminators.get(m, "?"))), file=deadXMLBuf)
    # , mod_order2):
    for s, n in sorted(l):
        print('      <when state="%s" next="%s"/>' % (s, n), file=deadXMLBuf)

    if m in compose.charActions:
        a = compose.charActions[m]
        if a in compose.statesByAction:
            for s in sorted(compose.statesByAction[a]):
                print('      <when state="%s" next="%s"/>' % ('_'.join(s), '_'.join(s+(a,))), file=deadXMLBuf)
        if a in compose.outputsByAction:
            for s, c1 in sorted(compose.outputsByAction[a]):
                print('      <when state="%s" output="%s"/>' % ('_'.join(s), xmlChar(c1)), file=deadXMLBuf)

    print('    </action>', file=deadXMLBuf)

print('    <action id="Multi_key">', file=deadXMLBuf)
print('      <when state="none" next="Multi_key"/>', file=deadXMLBuf)
print('    </action>', file=deadXMLBuf)
print(file=deadXMLBuf)
print('    <action id="">', file=deadXMLBuf)
print('      <when state="none" output=""/>', file=deadXMLBuf)
print('    </action>', file=deadXMLBuf)

print("  </actions>", file=deadXMLBuf)


def termChar(s):
    if len(compose.char(s)) > 1:
        return xmlChar(compose.terminators.get(compose.char(s), "?"))
    return xmlChar(compose.terminators.get(compose.char(s), compose.char(s)))


print(file=deadXMLBuf)
print(file=deadXMLBuf)
print('  <terminators>', file=deadXMLBuf)
# , mod_order):
for m in sorted(dmm):
    if m != tuple():
        output = ''.join([xmlChar(terminators.get(n, "?")) for n in m])
        print('    <when state="%s" output="%s"/>' % ('_'.join(m), output), file=deadXMLBuf)
for ss in sorted(compose.states):
    C = ''.join([termChar(s) for s in ss])
    s = '_'.join(list(ss))
    print('    <when state="%s" output="%s"/>' % (s, C), file=deadXMLBuf)
print('  </terminators>', file=deadXMLBuf)

deadXMLCode = deadXMLBuf.getvalue()
deadXMLBuf.close()

if __name__ == "__main__":
    print(deadXMLCode)
