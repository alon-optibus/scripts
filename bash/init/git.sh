#!/bin/bash

EDITOR=gedit

export REPO=$(basename "`git rev-parse --show-toplevel`")
export m='master'
export DEFAULT_BRANCH=$m

alias s='git status -s'
alias m='gco $m'
alias p='git push'
alias pf='git push -f'
alias cb='b=$(current_branch); type_var b'
alias k='gitk'
alias ka='gitk --all'
alias gl='py3 $py3_tools/git/list_commits.py'
alias wip="git add --all && git commit -a -m 'wip $(nows)'"
alias gr='git fetch origin && git reset --hard origin/$(current_branch)'
alias gpr='git_pull_rebase'
alias gprb='git_pull_rebase $b'
alias gm='git_merge'
alias m2m='m; gm $b'
alias lm='list_modified'
alias lmp='list_modified_py'

########################################################################################################################


current_branch() {
    git rev-parse --abbrev-ref HEAD
}


rename(){
  if [ -z "$2" ]; then
    echo 'Changing branch name to ' $1
    git branch -m $1
  else
    echo 'Changing branch name from ' $1 ' to ' $2
    git branch -m $1 $2
  fi
}


git_pull_rebase() {
    if [ -z "$1" ]; then
        git pull --rebase origin $DEFAULT_BRANCH
    else
        git pull --rebase origin $1
    fi
}


git_merge() {
  if [ -z "$1" ]; then
    echo "Usage: gm <branch_name>"
  else
    if [[ "$(current_branch)" != "$1" ]]; then
      git_reset force && git merge --no-ff $1
    fi
  fi
}


list_modified(){
  if [ -z "$1" ]
  then
    git diff --name-only
  else
    git diff --cached --name-only origin/$1
  fi
}

list_modified_py(){
  list_modified "$1" | grep --color='never' '.py'
}

ap8m(){

  files=$(list_modified_py "$1")

  if [ -z $files ]
  then
    return
  fi

  while IFS= read -r line
  do
    if [ -n "$line" ]
    then
      ap8 "$line"
    fi
  done <<< "$files"
}

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

type_var REPO
cb
print_break

info_git(){
  print_break
  type_var REPO
  type_var b
  info_bash
  display_info git
  print_break
}

alias info="info_git"

########################################################################################################################
