#!/bin/bash

########################################################################################################################

source $ROOT/.bash_profile
source $SCRIPTS/bash/init/git.sh

########################################################################################################################

export d='develop'

alias d='gco $d'

alias p8='envp; TEST=true py2 -m unittest euclid.tests.long_tests.utils.test_pep8.Pep8Test.test_pep8_conformance'
alias p8m='envp; TEST=true py2 -m unittest euclid.tests.long_tests.utils.test_pep8.Pep8Test.test_pep8_conformance_modified_only'

########################################################################################################################

echo

echo "d           : check-out to branch develop"
echo "hf          : check-out to branch hotfix"
echo "rc          : check-out to branch rc"
echo 'gbji "name" : create branch `jenkins-ignore--name`'
echo "p8          : run pep8 test"
echo "p8m         : run pep8 test on modified"

print_break

########################################################################################################################
