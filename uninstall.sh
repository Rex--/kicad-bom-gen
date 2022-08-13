#! /bin/sh
# The uninstallation procedure just removes the kicad-bom-gen/ directory.

INSTALL_PATH="$HOME/.local/share/kicad/6.0/plugins/kicad-bom-gen"

rm -r $INSTALL_PATH
