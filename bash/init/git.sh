#!/bin/bash

EDITOR=gedit

alias s='git status'
alias p='git push'
alias pf='git push -f'
alias cb='b=$(current_branch)'
alias k='gitk'
alias ka='gitk --all'
alias gl='py3 $py3_tools/print_git_log.py'
alias wip="git add --all && git commit -a -m 'wip $(nows)'"
alias gprb='git_pull_rebase $b'

# list git branches by last commit date:
alias bb='py3 $SCRIPTS/py3/tools/git/branch_list_by_date.py'


b(){
  if [ -z "$1" ]; then
		gco $b
	else
    # select the i'th branch by last commit date
		py3 $SCRIPTS/py3/tools/git/gco_by_date_index.py $1
	fi
}

export REPO=$(basename `git rev-parse --show-toplevel`)


########################################################################################################################

cb

echo "REPO = '$REPO'"
echo
bb

print_break

echo "[git status]"
s
print_break
echo "[git log]"
gl

print_break

echo "[bush commands]"
echo 's           : print git status'
echo 'p           : push'
echo 'pf          : push force'
echo 'cb          : set `$b` to current branch'
echo 'k           : run `gitk`'
echo 'ka          : run `gitk --all`'
echo "gl [n=10]   : print n last lines from git log"
echo "bb [n=10]   : list n git branches by last commit date. (if n==0: list all)"
echo 'b [i]       : check-out to the i`th branch by last commit date. (without i: check-out to branch $b)'
echo 'gco "name"  : check-out to branch `name`'
echo 'gpr "name"  : git_pull_rebase "name"'
echo 'gprb        : git_pull_rebase "$b"'
echo 'gb "name"   : create branch `name`'

########################################################################################################################
