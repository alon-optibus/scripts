#!/usr/bin/env bash

source bash_utils.sh

########################################################################################################################

cd_create "$WINDOWS_DIR/programs/netfx_setupverifier_new"
wget 'https://msdnshared.blob.core.windows.net/media/2018/05/netfx_setupverifier_new.zip'
unzip_remove netfx_setupverifier_new.zip

########################################################################################################################
