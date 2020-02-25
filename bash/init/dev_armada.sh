#!/bin/bash

########################################################################################################################

source $ROOT/.bash_profile
source $SCRIPTS/bash/init/git.sh

########################################################################################################################

alias p8='envp; TEST=true py2 -m unittest euclid.tests.long_tests.utils.test_pep8.Pep8Test.test_pep8_conformance'
alias p8m='envp; TEST=true py2 -m unittest euclid.tests.long_tests.utils.test_pep8.Pep8Test.test_pep8_conformance_modified_only'

alias m2d='gd; gm $b'
alias gprb='git_pull_rebase $b'

export d='develop'

alias d='gco $d'


########################################################################################################################

echo

alias gd
alias hf
alias rc
alias m2d
alias gprb

echo

echo "p8   : run pep8 test"
echo "p8m  : run pep8 test on modified"
echo "gbji : gb jenkins-ignore--<branch_name>"

print_break
echo "Workflow for merge to develop: gpr; m2d; Ctrl+x; p"
print_break

venv

########################################################################################################################
