#!/bin/bash

########################################################################################################################

source $SCRIPTS/bash/armada_utils.sh

unalias gd
unalias hf
unalias rc

########################################################################################################################

alias vip='py2 "$RESEARCH/alon/experiments/vip/ex_vip__benchmark.py"'

########################################################################################################################

source $SCRIPTS/bash/init/git.sh

info_research(){
    info_git
    print_break
    display_info dev_research
}

alias info="info_research"

########################################################################################################################
