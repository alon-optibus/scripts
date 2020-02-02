#!/usr/bin/env bash

source local_paths.sh
# export HOME, ROOT, SCRIPTS, DATA_DIR, WINDOWS_DIR

program_dir="$WINDOWS_DIR/programs/KeePass2"

########################################################################################################################

cd $program_dir || exit

#wine KeePass.exe
env WINEPREFIX=$HOME/winedotnet wine KeePass.exe

########################################################################################################################
