#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Génération du clavier pour mac os à partir d'un fichier xkb
#
# Copyright (C) 2017 Gaëtan Lehmann <gaetan.lehmann@gmail.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#

import codecs
import sys

import defaults
defaults.xkbFile = sys.argv[1]

import xkb
import dead_keys

xkb.tmplValues["actionsAndTerminators"] = dead_keys.deadXMLCode
for k, v in xkb.tmplValues.items():
    xkb.tmplValues[k] = dead_keys.xmlChar(v)
out = codecs.open(sys.argv[2], "w", "utf8")
out.write(xkb.tmpl % xkb.tmplValues)
