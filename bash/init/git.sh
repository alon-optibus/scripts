#!/bin/bash

EDITOR=gedit

export REPO=$(basename `git rev-parse --show-toplevel`)

alias s='git status'
alias p='git push'
alias pf='git push -f'
alias cb='b=$(current_branch)'
alias k='gitk'
alias ka='gitk --all'
alias gl='py3 $py3_tools/git/list_commits.py'
alias wip="git add --all && git commit -a -m 'wip $(nows)'"
alias gprb='git_pull_rebase $b'


########################################################################################################################
# list and name git branches by last commit date:

export _BRANCH_VAR_COUNT=0

bb(){

  # print list:
  py3 $SCRIPTS/py3/tools/git/branch_list_by_date.py "$@"

  # clear old variables:
  for i in `seq 1 $_BRANCH_VAR_COUNT`; do
    export b$i=
  done

  # set new variables:
  i=0
  while IFS= read -r line; do
      export b$i="$line"
      let i=i+1
  done <<< "$(py3 $SCRIPTS/py3/tools/git/branch_name_list_by_date.py "$@")"

  export _BRANCH_VAR_COUNT=$i
}

########################################################################################################################


alias b='gco $b'

alias b0='gco $b0'
alias b1='gco $b1'
alias b2='gco $b2'
alias b3='gco $b3'
alias b4='gco $b4'
alias b5='gco $b5'
alias b6='gco $b6'
alias b7='gco $b7'
alias b8='gco $b8'
alias b9='gco $b9'


########################################################################################################################

cb

echo "REPO = '$REPO'"
echo
bb -n 10

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
echo 'b[i]        : check-out to the i`th branch by last commit date. (without i: check-out to branch $b)'
echo 'gco "name"  : check-out to branch `name`'
echo 'gpr "name"  : git_pull_rebase "name"'
echo 'gprb        : git_pull_rebase "$b"'
echo 'gb "name"   : create branch `name`'

########################################################################################################################
