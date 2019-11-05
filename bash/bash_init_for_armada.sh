#!/bin/bash

source ~/scripts/bash/bash_init_for_git.sh

alias p8='cd $ROOT/euclid/euclid/tests/long_tests; envp; TEST=true python -m unittest test_pep8.Pep8Test.test_pep8_conformance'
alias p8

alias p8m='cd $ROOT/euclid/euclid/tests/long_tests; envp; TEST=true python -m unittest test_pep8.Pep8Test.test_pep8_conformance_modified_only'
alias p8m

echo ==================================================================================================================
echo "Workflow for merge to develop: gpr; m2d; Ctrl+x; p"
echo ==================================================================================================================

venv
