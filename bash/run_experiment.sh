#!/usr/bin/env bash

source bash_utils.sh
# export HOME, ROOT, SCRIPTS, DATA_DIR, WINDOWS_DIR

source wm_utils_1.sh

########################################################################################################################

#source "$SCRIPTS/bash/experiments/xdotool/ex_xd_002.sh"
#py3 $SCRIPTS/py3/experiments/xdotool/_001.py

########################################################################################################################

sleep 0.5

#o="$(xprop -id $wm_pid '\t$0' _NET_WM_NAME | cut -f 2)"

new_tab='"New Tab - Google Chrome"'

if [ "$wm_name" != "$new_tab" ]
then
  o="ne\n$wm_name != \n$new_tab"
else
  o="eq\n$wm_name = \n$new_tab"
fi

msgbox "$wm_pid\n\n$o"

#py3 "$SCRIPTS/py3/experiments/window_manager/ex_wm_001.py"

#wm_pid="$(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2)"
#wm_class="$(xprop -id $wm_pid '\t$0' WM_CLASS | cut -f 2)"
#wm_class="$(xprop -id $wm_pid WM_CLASS)"
#wm_class="$(xprop -id $wm_pid WM_CLASS | cut -d "=" -f 2)"

#msgbox "$wm_pid\n\n$wm_class"

#zenity --info --text="$(xdotool getwindowfocus getwindowname)"
#zenity --info --text="$(xprop -id $(xprop -root 32x '\t$0' _NET_ACTIVE_WINDOW | cut -f 2) WM_CLASS)"

########################################################################################################################
