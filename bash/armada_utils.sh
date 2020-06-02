#!/usr/bin/env bash

########################################################################################################################

source $ROOT/.bash_profile

alias a='cdi $ROOT'
alias r='cdi $RESEARCH'

pip_install_requirements(){
    pipu
    pip2r "$ROOT/euclid/requirements.txt"
    pip2cr "$ROOT/euclid/requirements.txt"
    pip2cr "$ROOT/euclid/cpython_requirements.txt"
    pip2vr "$ROOT/euclid/requirements.txt"
}

########################################################################################################################
