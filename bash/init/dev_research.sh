#!/bin/bash

########################################################################################################################

source $ROOT/.bash_profile

unalias gd
unalias hf
unalias rc

########################################################################################################################

export m='master'

alias m='gco $m'
alias gprb='git_pull_rebase $b'

########################################################################################################################

git_reset ()
{
    if [[ "$1" == "force" ]]; then
        git fetch origin $m && git reset --hard origin/$(current_branch);
    else
        smart_read "Are you sure you want to reset branch $(current_branch) (y/n)? ";
        echo;
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            git fetch origin && git reset --hard origin/$(current_branch);
        fi;
    fi
}

git_merge ()
{
    if [ -z "$1" ]; then
        echo "No branch was passed.  Usage gm <branch_name>";
    else
        if [[ "$(current_branch)" == "$m" ]]; then
            smart_read "Merging the branch will reset any changes you might have (but shouldn't have) on the $m branch, do you want to continue (y/n)? ";
            echo;
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                git_reset force && git merge --no-ff $1;
            fi;
        else
            echo "Must be on the $m branch to merge to $m (use gd to go to $m).  To merge to another branch use git merge directly";
        fi;
    fi
}


alias gm='git_merge'
alias m2m='m; gm $b'

########################################################################################################################

git_pull_rebase ()
{
    if [ -z "$1" ]; then
        git pull --rebase origin $m;
    else
        git pull --rebase origin $1;
    fi
}

########################################################################################################################

source $SCRIPTS/bash/init/git.sh

echo

alias m
alias gprb

print_break

alias_and_type sevip3 'cdi alon/experiments/sevip/_003'

print_break

########################################################################################################################
