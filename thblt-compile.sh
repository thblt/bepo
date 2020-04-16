#!/usr/bin/env bash

INSTALL_DIR=~/.config/sway

mkdir -p output

cd $(dirname $0)

confgen() {
    BEPO_LAYOUT_DESCRIPTION=layout_thblt.conf \
                           BEPO_VERSION="ariant: thblt 2" \
                           configGenerator/configGenerator.pl $@
}

confgen x_xkb_user > output/bepo_thblt.xkb

patch output/bepo_thblt.xkb bepo_thblt.xkb.patch

if [ "$1" = "install" ]; then
    cp output/bepo_thblt.xkb $INSTALL_DIR
    echo Copied to $INSTALL_DIR
fi
