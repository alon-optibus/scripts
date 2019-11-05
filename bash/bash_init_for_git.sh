#!/bin/bash

EDITOR=gedit

alias ww='piw; wip'
alias s='git status'
alias p='git push'
alias pf='git push -f'
alias lb='git branch --list'
alias cb='b=$(current_branch)'
alias b='gco $b'
alias m2d='gd; gm $b'
alias k='gitk'
alias ka='gitk --all'
alias gl='py3 $py3_tools/print_git_log.py'

cb

echo "b = $b"

echo ==================================================================================================================

echo "[git status]"
s
echo ==================================================================================================================
echo "[git log]"
gl

echo ==================================================================================================================

echo "[aliases]"
alias gd
alias hf
alias rc
alias ww
alias s
alias p
alias pf
alias lb
alias cb
alias b
alias m2d
alias k
alias ka
alias gl
