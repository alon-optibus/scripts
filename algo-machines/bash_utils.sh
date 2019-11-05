#!/bin/bash

########################################################################################################################

source $ROOT/.bash_profile

########################################################################################################################

zipr(){
	if [ -d "$1" ]
	then zip -r "$1.zip" $1
	elif [ -f "$1" ]
	then zip "$1.zip" $1
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

	get_files_from_efs sixflags $1 /data/euclid/combination_duty_pool/
}


get_files_from_titus(){

	export NAME=titus.clusters.optibus.co
	export API_SERVER=https://api.titus.clusters.optibus.co
	export ENV=titus

	kubectl config set-cluster $NAME --server $API_SERVER --insecure-skip-tls-verify=true
	kubectl config set-credentials $ENV-developer --client-key=$HOME/$ENV-developer.key --client-certificate=$HOME/$ENV-developer.crt
	kubectl config set-context $NAME --cluster $NAME --user $ENV-developer
	kubectl config use-context $NAME

	get_files_from_efs titus $1 /data/euclid/combination_duty_pool/
}


reset-path(){
	export PATH=$BASE_PATH
}


deactivate_conda(){
	if [ ! -z "$CONDA_EXE" ]; then
		
		conda deactivate
		
		unset -f conda
		
		reset-path
		
	fi
}


envpy3(){
	
	if [ ! -z "$VIRTUAL_ENV" ]; then
		deactivate
	fi
	
	source ~/anaconda3/bin/activate
}

alias imut='sudo chattr +i'
alias mut='sudo chattr -i'
alias cpi='envcp; ipython'
alias cpi-s3='envcp; ipython -i ~/dev/research/alon/AlgoBucketInteractive.py'
alias r='cd ~/dev/research/'

alias read-log='envpy3; ipython -i ~/scripts/read_log.py'

alias sagi='sudo apt-get install'

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

s3has(){
	python ~/scripts/s3has.py $1
}

s3has-deault(){
	python ~/scripts/s3has_default.py $1
}


s3del(){
	python ~/scripts/s3del.py $1
}

s3del-deault(){
	python ~/scripts/s3del_default.py $1
}

s3key(){
	python ~/scripts/s3key.py $1
}

alias s3put='python ~/scripts/s3put.py'
alias s3get='python ~/scripts/s3get.py'
alias s3del='python ~/scripts/s3del.py'

#####################################################################################################

export BASE_PATH=$PATH

#####################################################################################################
