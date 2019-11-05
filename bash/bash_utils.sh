#!/usr/bin/env bash

########################################################################################################################

source local_bash_utils.sh

export py2_scripts=$SCRIPTS/py2
export py2_tools=$py3_scripts

export py3_scripts=$SCRIPTS/py3
export py3_tools=$py3_scripts/tools

source $ROOT/.bash_profile

unalias env3

########################################################################################################################

export BASE_PATH=$PATH

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

#alias read-log='envpy3; ipython -i $py3_tools/read_log.py'

alias sagi='sudo apt-get install'
alias sedit='sudo gedit'

alias venv='deactivate_conda; source ~/dev/venv/bin/activate'
alias envp='deactivate_conda; source ~/dev/envp/bin/activate'
alias envcp='deactivate_conda; source ~/dev/envcp/bin/activate'

alias lam1='lam 1'
alias lam2='lam 2'
alias lam3='lam 3'

alias mam1='mam 1 /m/1'  # mount algo-machine 1
alias mam2='mam 2 /m/2'  # mount algo-machine 2
alias mam3='mam 3 /m/3'  # mount algo-machine 3

alias unmam1='sudo umount /m/1'  # unmount algo-machine 1
alias unmam2='sudo umount /m/2'  # unmount algo-machine 2
alias unmam3='sudo umount /m/3'  # unmount algo-machine 3

alias pause='read -n1 -r -p "Press any key to continue... " key; echo ""'

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
