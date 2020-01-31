#!/usr/bin/env bash

source bash_utils.sh
# export HOME, ROOT, RESEARCH, SCRIPTS, DATA_DIR, WINDOWS_DIR

########################################################################################################################

alias_and_type(){
  alias $1="$2"
  echo "$(alias $1)  # $3"
}

type_var(){
  echo $1=${!1}
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
  init
}

alias r='cdi $RESEARCH'
alias a='cdi $ROOT'
alias a='cdi $SCRIPTS'

########################################################################################################################

# display system information:
lsb_release -a
print_break

# run './~bash_init~' if exists:
init_local

# interrupt with 'ctrl+j' instead of 'ctrl+c':
stty intr ^J

########################################################################################################################
