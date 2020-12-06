#!/usr/bin/env bash

WM_CLASS_CHROME="google-chrome"

source wm_utils_1.sh

if [ "$wm_class" = "$WM_CLASS_CHROME" ]
then

  sleep 0.2

  xdotool mousemove 0 0

  if [ "$wm_name" != "New Tab - Google Chrome" ]
  then
    xdotool key ctrl+t
  fi

  xdotool key alt+f b

fi

########################################################################################################################
