#!/bin/sh -x

./configGenerator.pl x_xkb_root > "results/layout.xkb"
./configGenerator.pl x_xkb_user > "results/layout-user.xkb"
./configGenerator.pl x_xmodmap  > "results/layout.xmodmap"
./configGenerator.pl x_compose  > "results/layout.XCompose"
./configGenerator.pl win_msklc_azerty | iconv -f utf-8 -t utf-16le > "results/bepoA-kbd.klc"
./configGenerator.pl win_msklc_bepo   | iconv -f utf-8 -t utf-16le > "results/bepoB-kbd.klc"
./configGenerator.pl win_msklc_qwertz | iconv -f utf-8 -t utf-16le > "results/bepoC-kbd.klc"
./configGenerator.pl win_msklc_azerty | iconv -f utf-8 -t utf-16 > "results/bepoA.klc"
./configGenerator.pl win_msklc_bepo   | iconv -f utf-8 -t utf-16 > "results/bepoB.klc"
./configGenerator.pl win_msklc_qwertz | iconv -f utf-8 -t utf-16 > "results/bepoC.klc"

./configGenerator.pl description > "results/layout-desc.html"

./map.py         "results/layout.xkb" "results/layout.txt"
./svg.py         "results/layout.xkb" "results/bepo"
./klavaro.py     "results/layout.xkb" "results/layout.kbd"
./ktouch.py      "results/layout.xkb" "results/layout.keyboard"
./typefaster.py  "results/layout.xkb" "results/layout.xml"
./keymaps.py     "results/layout.xkb" "results/layout.map"
./keymaps.py -u  "results/layout.xkb" "results/layout.utf8.map"
./kbdmap.py      "results/layout.xkb" "results/layout.kbdmap"
./wscons.py      "results/layout.xkb" "results/layout.wscons"
./macosx.py      "results/layout.xkb" "results/layout.keylayout"
./keytables.py   "results/layout.xkb" "results/layout.keytables"

perl -p -e 's#\tinclude "pc\(pc105\)"#\tinclude "pc/pc(pc105)"#g' "results/layout-user.xkb" > "results/layout-user-legacy.xkb"
