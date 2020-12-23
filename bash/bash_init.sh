#!/usr/bin/env bash

source bash_utils.sh
# export HOME, ROOT, RESEARCH, SCRIPTS, DATA_DIR, WINDOWS_DIR

########################################################################################################################

alias_and_type(){
  alias $1="$2"
  echo "$(alias $1)  # $3"
}

type_var(){
  echo "$1 = '${!1}'"
}

init_local(){
  if [ -f "~bash_init~" ]
  then source ./~bash_init~
  elif [ -f "__bash_init.sh" ]
  then source ./__bash_init.sh
  fi
}

cdi(){
  cd "$1" || return
  init_local
}

alias r='cdi $RESEARCH'
alias a='cdi $ROOT'
alias s='cdi $SCRIPTS'

unalias zipr

zipr(){
    if [ -z "$1" ]
    then
    display_info zipr
    else
    py3 $SCRIPTS/py3/tools/zipr.py "$@"
    fi
}

########################################################################################################################

display_info(){
    cat "$SCRIPTS/bash/info/$1.txt"
    echo
}

info_system(){
    # display system information:
    lsb_release - a
}

info_paths(){
    echo "[environment variables]"
    echo "HOME              : home directory ('$HOME')"
    echo "ROOT              : armada dev directory ('$ROOT')"
    echo "RESEARCH          : research directory ('$RESEARCH')"
    echo "SCRIPTS           : scripts directory ('$SCRIPTS')"
    echo "DATA_DIR          : data directory ('$DATA_DIR')"
    echo "ARCHIVE_DIR       : data directory ('$ARCHIVE_DIR')"
}

info_interactive(){
    echo "[interactive bush commands]"
    echo "init : init with local context"
    echo "a    : init armada context in '\$ROOT' ('$ROOT')"
    echo "r    : init research context in '\$RESEARCH' ('$RESEARCH')"
    echo "s    : init scripts context in '\$SCRIPTS' ('$SCRIPTS')"
}

info_bash(){
    info_system
    print_break
    info_paths
    print_break
    display_info bash
    print_break
    info_interactive
}

alias info='info_bash'
alias am='display_info am'
alias s3='display_info s3'
alias piph='display_info pip'

########################################################################################################################

# call info function
alias ?='print_break;info;print_break'
echo '?: display info'
print_break

# run './~bash_init~' if exists:
init_local

# interrupt with 'ctrl+j' instead of 'ctrl+c':
stty intr ^J

source local_bash_init.sh

########################################################################################################################
