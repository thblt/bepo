#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Les terminateurs pour les touches mortes
#
# Copyright (C) 2008 Gaëtan Lehmann <gaetan.lehmann@jouy.inra.fr>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#


terminators = {
    "abovedot": "˙",
    "acute": "´",
    "bar": "-",
    "belowdot": "̣",
    "breve": "˘",
    "caron": "ˇ",
    "cedilla": "¸",
    "circumflex": "^",
    "circumflexbelow": "̭",
    "commabelow": ",",
    "currency": "¤",
    "diaeresis": "¨",
    "diaeresisbelow": "̤",
    "doubleacute": "˝",
    "grave": "`",
    "hook": "̉",
    "horn": "̛",
    "invertedbreve": "̑",
    "linebelow": "_",
    "macron": "¯",
    "ogonek": "˛",
    "retroflexhook": "̢",
    "righthalfring": "ʾ",
    "ringabove": "°",
    "ringbelow": "̥",
    "sci": "∞",
    "stroke": "/",
    "tilde": "~",
    "tildebelow": "̰",
    "topbar": "⁻",
    "Multi_key": "↯",
    "greek": "µ",
}

spaceTerminators = dict(terminators)
spaceTerminators["diaeresis"] = '"'
spaceTerminators["acute"] = "'"

combiningTerminators = {
    "abovedot": "̇",
    "acute": "́",
    "bar": "-",
    "belowdot": "̣",
    "breve": "̆",
    "caron": "̌",
    "cedilla": "̧",
    "circumflex": "̂",
    "circumflexbelow": "̭",
    "commabelow": "̦",
    "currency": "¤",
    "diaeresis": "̈",
    "diaeresisbelow": "̤",
    "doubleacute": "̋",
    "doublegrave": "̏",
    "grave": "̀",
    "hook": "̉",
    "horn": "̛",
    "invertedbreve": "̑",
    "linebelow": "_",
    "macron": "̄",
    "ogonek": "̨",
    "retroflexhook": "̢",
    "righthalfring": "ʾ",
    "ringabove": "̊",
    "ringbelow": "̥",
    "sci": "∞",
    "stroke": "̸",
    "tilde": "̃",
    "tildebelow": "̰",
    "topbar": "⁻",
    "greek": "µ",
}
