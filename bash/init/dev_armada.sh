#!/bin/bash

########################################################################################################################

source $SCRIPTS/bash/armada_utils.sh
source $SCRIPTS/bash/init/git.sh

########################################################################################################################

export d='develop'
export DEFAULT_BRANCH=$d

alias d='gco $d'
alias test_vip_q='echo "quick test for VIP:"; TEST=true py2 -m unittest euclid.tests.quick_tests.test_vehicle_mip_scheduler 2>&1 | tail -n 5'
alias test_vip_l='echo "long test for VIP:"; TEST=true py2 -m unittest euclid.tests.long_tests.scheduling.test_vehicle_mip 2>&1 | tail -n 5'
alias test_vip='test_vip_q; test_vip_l;'
alias _ap8='py3 -m autopep8 -v --global-config "$ROOT/euclid/setup.cfg"'
alias ap80='ap8 --select=W2,W3,E305,E306'
alias p8='TEST=true py2 -m unittest euclid.tests.long_tests.utils.test_pep8.Pep8Test.test_pep8_conformance'
alias p8m='TEST=true py2 -m unittest euclid.tests.long_tests.utils.test_pep8.Pep8Test.test_pep8_conformance_modified_only'

########################################################################################################################

ap80m(){
  while IFS= read -r line
  do
    ap80 "$line" | grep --regexp="--->" --before-context=1
  done <<< "$(list_modified_py "$1")"
  p8m
}

########################################################################################################################

info_armada(){
  info_git
  display_info dev_armada
  print_break
}

alias info="info_armada"

########################################################################################################################
