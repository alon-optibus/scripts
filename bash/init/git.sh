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

# list git branches by last commit date:
alias bb='py3 $SCRIPTS/py3/tools/git/branch_list_by_date.py'

bbh(){
  # show n last committed branches
  if [ -z "$1" ]; then
		bb | head
	else
		bb | head -n $1
	fi
}


bbt(){
  # show n oldest committed branches
  if [ -z "$1" ]; then
		bb | tail
	else
		bb | tail -n $1
	fi
}


b(){
  if [ -z "$1" ]; then
		gco $b
	else
    # select the i'th branch by last commit date
		py3 $SCRIPTS/py3/tools/git/gco_by_date_index.py $1
	fi
}


########################################################################################################################

cb

echo "b = $b"

print_break

echo "[git status]"
s
print_break
echo "[git log]"
gl

print_break

echo "[aliases]"
alias s
alias p
alias pf
alias lb
alias cb
alias b
alias k
alias ka
alias gl

echo "bb [n]: list n git branches by last commit date. (without n: list all)"
echo "gcoi [i]: select the i'th branch by last commit date. (without i: list 10 branches by last commit date)"

########################################################################################################################
