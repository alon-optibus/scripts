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

zipr(){
	if [ -d "$1" ]
	then zip -r "$1.zip" "$1"
	elif [ -f "$1" ]
	then zip "$1.zip" "$1"
	else echo "$1" not found.
	fi
}


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


env3(){
	
	if [ -n "$VIRTUAL_ENV" ]; then
		deactivate
	fi

	export PYTHONPATH=$py3_scripts
	
	source $HOME/anaconda3/bin/activate
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

get_algo_machine_external_ip(){
    if [ -z "$1" ]; then
        IP_ADDRESS=$AM1_IP_ADDRESS
        echo "Default algo machine is number 1"
    else
    	echo "Requested algo machine is number $1"
    	if [ $1 == 1 ]; then
    		IP_ADDRESS=$AM1_IP_ADDRESS
	    elif [ $1 == 2 ]; then
	    	IP_ADDRESS=$AM2_IP_ADDRESS
	    elif [ $1 == 3 ]; then
	    	IP_ADDRESS=$AM3_IP_ADDRESS
	    else
	    	echo "No algo machine number $1, contact an algo team member to create new machines (if really needed)"
	    	return
	    fi
	  echo "Machine ip adress is $IP_ADDRESS"
	fi

}

get_algo_machine_internal_ip(){
    if [ -z "$1" ]; then
        IP_ADDRESS=$AM1_INTERNAL_IP_ADDRESS
        echo "Default algo machine is number 1"
    else
        echo "Requested algo machine is number $1"
        if [ $1 == 1 ]; then
            IP_ADDRESS=$AM1_INTERNAL_IP_ADDRESS
        elif [ $1 == 2 ]; then
            IP_ADDRESS=$AM2_INTERNAL_IP_ADDRESS
        elif [ $1 == 3 ]; then
            IP_ADDRESS=$AM3_INTERNAL_IP_ADDRESS
        else
            echo "No algo machine number $1, contact an algo team member to create new machines (if really needed)"
            return
        fi
      echo "Machine ip adress is $IP_ADDRESS"
    fi

}

get_algo_machine_ip(){
    if [ -z "$1" ]; then
        MACHINE_NUMBER=1
    else
        MACHINE_NUMBER=$1
    fi
    echo "USER is $USER"
    if [ $USER == 'ubuntu' ]; then
        echo "Working with internal ips of the machines"
        get_algo_machine_internal_ip $MACHINE_NUMBER
    else
        echo "Working with external ips of the machines"
        get_algo_machine_external_ip $MACHINE_NUMBER
    fi
}

get_file_from_algo_machine(){
    get_algo_machine_ip $1
    if [ -z "$3" ]; then
        TARGET_FOLDER='~'
    else
        TARGET_FOLDER=$3
    fi
    echo "scp -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem ubuntu@$IP_ADDRESS:$2 $TARGET_FOLDER"
    scp -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem ubuntu@$IP_ADDRESS:$2 $TARGET_FOLDER
}


send_file_to_algo_machine(){
    get_algo_machine_ip $1
    if [ -z "$3" ]; then
        TARGET_FOLDER='/home/ubuntu/'
    else
        TARGET_FOLDER=$3
    fi
    echo "scp -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem $2 ubuntu@$IP_ADDRESS:$TARGET_FOLDER"
    scp -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem $2 ubuntu@$IP_ADDRESS:$TARGET_FOLDER
}


log_to_algo_research_machine() {
    echo $1
	get_algo_machine_ip $1
	echo "Enjoy"
	cmd="ssh -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem -q ubuntu@$IP_ADDRESS"
	echo $cmd
	$cmd

}

ping_algo_machine(){
	RED='\033[0;31m'
	GREEN='\033[0;32m'
	NC='\033[0m' # No Color
	if [ -z "$IP_ADDRESS" ]; then
		get_algo_machine_ip $1
		COUNTER=$1
	fi
	if [ -z "$IP_ADDRESS" ]; then
		return
	fi
	if ping -c1 -w3 $IP_ADDRESS >/dev/null 2>&1
	then
	    echo -e "Algo machine $COUNTER IP $IP_ADDRESS is ${GREEN}on${NC}" >&2
	else
	    echo -e "Algo machine $COUNTER IP $IP_ADDRESS is ${RED}off${NC}" >&2
	fi
	IP_ADDRESS=""
}

ping_all_algo_machines(){
	ONE=1
	COUNTER=1
	for IP_ADDRESS in $AM1_IP_ADDRESS $AM2_IP_ADDRESS $AM3_IP_ADDRESS
	do
		ping_algo_machine $IP_ADDRESS

		let "COUNTER = $COUNTER + $ONE"
	done
}

ping_algo_machines(){
	if [ -z "$1" ]; then
		ping_all_algo_machines
	else
		ping_algo_machine $1
	fi
}

mount_algo_machine(){
	get_algo_machine_ip $1
	echo 'sshfs -o ssh_command="ssh -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem" ubuntu@$IP_ADDRESS:/ /m/$1'
	sshfs -o ssh_command="ssh -oStrictHostKeyChecking=no -i ~/.ssh/optiprod.pem" ubuntu@$IP_ADDRESS:/ /m/$1
}

alias lam='log_to_algo_research_machine'
alias pam='ping_algo_machines'
alias mam='mount_algo_machine'
alias gfm='get_file_from_algo_machine'
alias sfm='send_file_to_algo_machine'

#####################################################################################################

#s3has(){
#	python $py2_tools/s3has.py $1
#}
#
#s3has-deault(){
#	python $py2_tools/s3has_default.py $1
#}
#
#
#s3del(){
#	python $py2_tools/s3del.py $1
#}
#
#s3del-deault(){
#	python $py2_tools/s3del_default.py $1
#}
#
#s3key(){
#	python $py2_tools/s3key.py $1
#}
#
#alias s3put='python $py2_tools/s3put.py'
#alias s3get='python $py2_tools/s3get.py'
#alias s3del='python $py2_tools/s3del.py'

#####################################################################################################
