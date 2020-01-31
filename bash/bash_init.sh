#!/usr/bin/env bash

source bash_utils.sh

########################################################################################################################

alias_and_type(){
  alias $1="$2"
  echo "$(alias $1)  # $3"
}

type_var(){
  echo $1=${!1}
}

alias init='source ./~bash_init~'

init_if_exists(){
  if [ -f "~bash_init~" ]
    then init
  fi
}

########################################################################################################################

# display system information:
lsb_release -a
print_break

# run './~bash_init~' if exists:
init_if_exists

# interrupt with 'ctrl+j' instead of 'ctrl+c':
stty intr ^J

########################################################################################################################
