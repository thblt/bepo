#!/bin/sh

cp "results/layout-user.xkb" ../xkb/bepo.xkb
cp "results/layout-user-legacy.xkb" ../xkb/bepo-xorglegacy.xkb
cp "results/layout.XCompose" ../xkb/XCompose

cp "results/bepoA.klc" ../windows/bepo-azerty.klc
cp "results/bepoB.klc" ../windows/bepo.klc
cp "results/bepoC.klc" ../windows/bepo-qwertz.klc
cp "results/layout.kbd" ../klavaro/bepo.kbd
cp "results/layout.keyboard" ../ktouch/bepo.keyboard
cp "results/layout.xml" ../typefaster/bepo.xml
cp "results/layout.map" ../keymaps/bepo.map
cp "results/layout.utf8.map" ../keymaps/bepo-utf8.map
cp "results/layout.kbdmap" ../kbdmap/bepo.kbd
cp "results/layout.wscons" ../wscons/bepo.map
cp "results/layout.keylayout" ../macosx/bepo.bundle/Contents/Resources/bepo.keylayout
cp "results/layout.keytables" ../keytables/bepo
