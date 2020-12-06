#!/usr/bin/env bash

WM_CLASS_CHROME="google-chrome"
CHROME_TITLE_SUFFIX=" - Google Chrome"

wmctrl -a "$CHROME_TITLE_SUFFIX"
sleep 0.2
source wm_utils_1.sh

if [ "$wm_class" != "$WM_CLASS_CHROME" ]
then
  nohup "google-chrome-stable" &>/dev/null &
fi


########################################################################################################################

#source wm_utils_1.sh
#
#sleep 0.2
#
#if [ $wm_class = '"google-chrome"' ]
#then
#  xdotool mousemove 0 0
#  xdotool key ctrl+t alt+f b
#fi

########################################################################################################################
