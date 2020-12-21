#!/usr/bin/env bash

########################################################################################################################

source $ROOT/.bash_profile

alias a='cdi $ROOT'
alias r='cdi $RESEARCH'

alias env_euclid='set -a; source "$LOCAL/env_euclid.env"; set +a'

pip_install_requirements(){
    pipu
    pip2pr "$ROOT/euclid/requirements.txt"
    pip2cr "$ROOT/euclid/requirements.txt"
    pip2cr "$ROOT/euclid/cpython_requirements.txt"
    pip2vr "$ROOT/euclid/requirements.txt"
}

########################################################################################################################
