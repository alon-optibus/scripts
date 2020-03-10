#!/usr/bin/env bash

########################################################################################################################

source local_bash_utils.sh
# export HOME, ROOT, RESEARCH, SCRIPTS, DATA_DIR, WINDOWS_DIR

export Downloads=~/Downloads

export py2_scripts=$SCRIPTS/py2
export py2_tools=$py3_scripts

export py3_scripts=$SCRIPTS/py3
export py3_tools=$py3_scripts/tools

########################################################################################################################

export BASE_PATH=$PATH

########################################################################################################################

alias cdd='cd $Downloads'
alias cds='cd $SCRIPTS'

alias print_break='printf "_______________________________________________________________________________________________\n\n"'

env-reset(){
  source /etc/environment
  export PYTHONPATH=
  source ~/.profile
}

########################################################################################################################

alias now='date +%s'

time_delta(){
  echo $(($(now)-$1))
}

alias nows='date "+%F %T"'

########################################################################################################################

path_create(){
  mkdir -p "$1"
}

path_remove(){
  rm -rf "$1"
}

cd_create(){
  path_create "$1"
  cd "$1" || exit
}

path_remove_pwd(){
  cd ..
  path_remove "$OLDPWD"
}

alias get_tmp_dir='mktemp -d -t my-XXXXXXXXXX'

cd_tmp_dir(){
  _tmp_dir=
  _tmp_dir=$(get_tmp_dir)
  echo _tmp_dir = "$_tmp_dir"
  cd "$_tmp_dir" || exit
}

path_unzip(){
  if [ $# -gt 1 ]
  then
    path_create "$2"
    unzip "$1" -d "$2"
  else
    unzip "$1"
  fi
}

unzip_remove(){
  path_unzip "$@"
  path_remove "$1"
}

########################################################################################################################

alias zipr='py3 $SCRIPTS/py3/tools/zipr.py'
# zip file or directory:
#   zipr "dir/name"                    : write to "dir/name.zip"
#   zipr "dir/name" "dst_name"         : write to "dir/dst_name.zip"
#   zipr "dir/name" "dst_dir"          : write to "dst_dir/name.zip"
#   zipr "dir/name" "dst_dir/dst_name" : write to "dst_dir/dst_name.zip"
#   {name} in `dst_name` replaced with `name`.
#   {stem} in `dst_name` replaced with `name` without suffix.
#   {time} in `dst_name` replaced with time-stamp (%Y-%m-%d_%H-%M-%S-%f).
#
#  If done successfully, the last line to be printed will be the path of the created zip file.
#  Otherwise, the last line to be printed will be empty.


arc(){
	if [ -d "$1" ]
	then zip -r "$ARCHIVE_DIR/$1_$(date +%Y-%m-%d_%H-%M).zip" "$1"
	elif [ -f "$1" ]
	then zip "$ARCHIVE_DIR/$1_$(date +%Y-%m-%d_%H-%M).zip" "$1"
	else echo "$1" not found.
	fi
}


get_files_from_sixflags(){

	export NAME=sixflags.clusters.optibus.co
	export API_SERVER=https://api.sixflags.clusters.optibus.co
	export ENV=sixflags

	kubectl config set-cluster $NAME --server $API_SERVER --insecure-skip-tls-verify=true
	kubectl config set-credentials $ENV-developer --client-key=$HOME/$ENV-developer.key --client-certificate=$HOME/$ENV-developer.crt
	kubectl config set-context $NAME --cluster $NAME --user $ENV-developer
	kubectl config use-context $NAME

	get_files_from_efs sixflags "$1" /data/euclid/combination_duty_pool/
}


get_files_from_titus(){

	export NAME=titus.clusters.optibus.co
	export API_SERVER=https://api.titus.clusters.optibus.co
	export ENV=titus

	kubectl config set-cluster $NAME --server $API_SERVER --insecure-skip-tls-verify=true
	kubectl config set-credentials $ENV-developer --client-key=$HOME/$ENV-developer.key --client-certificate=$HOME/$ENV-developer.crt
	kubectl config set-context $NAME --cluster $NAME --user $ENV-developer
	kubectl config use-context $NAME

	get_files_from_efs titus "$1" /data/euclid/combination_duty_pool/
}


reset-path(){
	export PATH=$BASE_PATH
}


deactivate_conda(){
	if [ -n "$CONDA_EXE" ]; then
		
		conda deactivate
		
		unset -f conda
		
		reset-path
		
	fi
}


sagi(){
  sudo apt-get install "$1"
  apt-cache policy "$1"
}

alias sedit='sudo gedit'

alias venv='deactivate_conda; source ~/dev/venv/bin/activate'
alias envp='deactivate_conda; source ~/dev/envp/bin/activate'
alias envcp='deactivate_conda; source ~/dev/envcp/bin/activate'

alias pause='read -n1 -r -p "Press any key to continue... " key; echo ""'

msgbox(){
  zenity --width=1600 --info --text="$1"
}

#####################################################################################################

alias lam='log_to_algo_research_machine'
alias pam='ping_algo_machines'
alias mam='mount_algo_machine'
alias gfm='get_file_from_algo_machine'
alias sfm='send_file_to_algo_machine'

alias am='less -FX "$SCRIPTS/info/am.txt"'

alias am_get='py3 $SCRIPTS/py3/tools/algo_machines/get_file_from_am.py'
alias am_put='py3 $SCRIPTS/py3/tools/algo_machines/put_file_in_am.py'
alias am_del='py3 $SCRIPTS/py3/tools/algo_machines/del_file_in_am.py'

am_ip(){
  if [ $1 == 1 ]; then
    echo $AM1_IP_ADDRESS
  elif [ $1 == 2 ]; then
      echo $AM2_IP_ADDRESS
  elif [ $1 == 3 ]; then
      echo $AM3_IP_ADDRESS
  fi
}

alias ssh_optiprod='ssh -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem -q'

am1(){
  ssh_optiprod ubuntu@$AM1_IP_ADDRESS "$@"
}

am2(){
  ssh_optiprod ubuntu@$AM2_IP_ADDRESS "$@"
}

am3(){
  ssh_optiprod ubuntu@$AM3_IP_ADDRESS "$@"
}

#####################################################################################################

alias s3='less -FX "$SCRIPTS/info/s3.txt"'

alias aws_login='saml2aws login --session-duration=32400'

alias s3_put_file='py3 $SCRIPTS/py3/tools/s3/put_file.py'
alias s3_get_file='py3 $SCRIPTS/py3/tools/s3/get_file.py'
alias s3_has_key='py3 $SCRIPTS/py3/tools/s3/has_key.py'
alias s3_has_mirror='py3 $SCRIPTS/py3/tools/s3/has_mirror.py'
alias s3_del_key='py3 $SCRIPTS/py3/tools/s3/del_key.py'
alias s3_del_mirror='py3 $SCRIPTS/py3/tools/s3/del_mirror.py'
alias s3_list_keys='py3 $SCRIPTS/py3/tools/s3/list_keys.py'
alias s3_list_mirror='py3 $SCRIPTS/py3/tools/s3/list_mirror.py'
alias s3_command_for_downlad='py3 $SCRIPTS/py3/tools/s3/get_download_command.py'
alias s3_get_mirror_key='py3 $SCRIPTS/py3/tools/s3/get_mirror_key.py'

s3_stream(){
  vaws s3 cp "s3://algo-research/$1" -
}

s3_stream_mirror(){
  s3_stream "$(s3_get_mirror_key $1)"
}

########################################################################################################################

alias grep_context_logger='grep -E "(>>>>|<<<<)"'

cat_context_logger(){
  cat "$1" | grep_context_logger
}

#####################################################################################################
