#!/bin/bash

EDITOR=gedit

alias s='git status'
alias p='git push'
alias pf='git push -f'
alias bb='git branch --list'
alias cb='b=$(current_branch)'
alias b='gco $b'
alias k='gitk'
alias ka='gitk --all'
alias gl='py3 $py3_tools/print_git_log.py'
alias wip="git add --all && git commit -a -m 'wip $(nows)'"

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

########################################################################################################################
