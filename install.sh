#! /bin/sh
# All the installation procedure does is copy the scripts to ~/.local/share/kicad

INSTALL_PATH="$HOME/.local/share/kicad/6.0/plugins/kicad-bom-gen"

# Make root directory if it doesn't exist
mkdir -p $INSTALL_PATH

# Copy scripts
cp bom-gen.py $INSTALL_PATH
cp bom-gen-pdf.py $INSTALL_PATH

# Copy templates
cp -r templates/ $INSTALL_PATH
