#!/usr/bin/env bash

source wm_utils_1.sh

if [ "$wm_class" = '"google-chrome"' ]
then

  sleep 0.2

  xdotool mousemove 0 0

  if [ "$wm_name" != '"New Tab - Google Chrome"' ]
  then
    xdotool key ctrl+t
  fi

  xdotool key alt+f b

fi

########################################################################################################################
